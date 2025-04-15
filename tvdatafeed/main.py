# tvdatafeed/main.py

import json
import time
import re
import pandas as pd
import websocket
from datetime import datetime
from .tvsession import TVSession


class Interval:
    in_1_minute = '1'
    in_5_minute = '5'
    in_15_minute = '15'
    in_1_hour = '60'
    in_4_hour = '240'
    in_1_day = '1D'


class TvDatafeed:
    def __init__(self, username=None, password=None, proxies=None):
        self.session = TVSession(username, password, proxies)
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://www.tradingview.com/'
        }

    def get_hist(self, symbol, exchange, interval=Interval.in_1_minute, n_bars=200):
        symbol = symbol.upper()
        exchange = exchange.upper()
        interval = interval

        session = 'ds_' + ''.join(re.sample('abcdefghijklmnopqrstuvwxyz0123456789', 12))
        chart_session = 'cs_' + ''.join(re.sample('abcdefghijklmnopqrstuvwxyz0123456789', 12))

        def send(ws, message):
            ws.send(f'{len(message)}\n{message}')

        def construct_message(func, param):
            return json.dumps({"m": func, "p": param}, separators=(',', ':'))

        def create_message(func, param):
            return f'{len(construct_message(func, param))}\n{construct_message(func, param)}'

        ws = websocket.create_connection("wss://data.tradingview.com/socket.io/websocket")

        send(ws, create_message("set_auth_token", ["unauthorized"]))
        send(ws, create_message("chart_create_session", [chart_session, "" + session]))
        send(ws, create_message("quote_create_session", [session]))
        send(ws, create_message("quote_add_symbols", [session, f'{symbol}:{exchange}']))
        send(ws, create_message("quote_fast_symbols", [session, f'{symbol}:{exchange}']))
        send(ws, create_message("resolve_symbol", [chart_session, "symbol_1", f"={exchange}:{symbol}"]))
        send(ws, create_message("create_series", [chart_session, "s1", "s", f"={exchange}:{symbol}", interval, n_bars]))

        df = pd.DataFrame(columns=['time', 'open', 'high', 'low', 'close', 'volume'])

        for _ in range(200):
            try:
                result = ws.recv()
                if 's1' in result and 'timescale' not in result:
                    matches = re.findall(r'\[\[(.*?)\]\]', result)
                    for match in matches:
                        fields = match.split(',')
                        if len(fields) < 6:
                            continue
                        ts = int(fields[0])
                        time_obj = datetime.fromtimestamp(ts)
                        row = {
                            'time': time_obj,
                            'open': float(fields[1]),
                            'high': float(fields[2]),
                            'low': float(fields[3]),
                            'close': float(fields[4]),
                            'volume': float(fields[5])
                        }
                        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
                    break
            except Exception:
                continue

        ws.close()
        return df
