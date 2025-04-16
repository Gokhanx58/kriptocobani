import os
import re
import json
import time
import pandas as pd
from datetime import datetime
from requests import Session
from websocket import create_connection
from .const import INTERVALS, SCREENER, GET_HISTORY_PAYLOAD, WEBSOCKET_HEADERS

class TvDatafeed:
    def __init__(self, auto_login=True):
        self.session = Session()
        self.token = None
        self.headers = {}
        self.ws = None

    def _create_connection(self):
        self.ws = create_connection("wss://prodata.tradingview.com/socket.io/websocket", header=WEBSOCKET_HEADERS)

    def _send_raw_message(self, message: str):
        self.ws.send(message)

    def _construct_message(self, session: str, chart_session: str, symbol: str, interval: str, n_bars: int):
        symbol_full = f"{SCREENER}:{symbol.upper()}"
        timestamp = int(time.time())
        payload = GET_HISTORY_PAYLOAD.copy()
        payload['symbol'] = symbol_full
        payload['resolution'] = INTERVALS[interval]
        payload['from'] = timestamp - n_bars * 60 * 60
        payload['to'] = timestamp

        msg = json.dumps({
            "m": "resolve_symbol",
            "p": [session, symbol_full]
        })
        self._send_raw_message(f"~m~{len(msg)}~m~{msg}")

        msg = json.dumps({
            "m": "create_series",
            "p": [chart_session, "s1", "s", symbol_full, interval, n_bars]
        })
        self._send_raw_message(f"~m~{len(msg)}~m~{msg}")

    def get_hist(self, symbol: str, exchange: str = 'BINANCE', interval: str = '1m', n_bars: int = 100):
        try:
            self._create_connection()
            session_id = f"qs_{int(time.time() * 1000)}"
            chart_session = f"cs_{int(time.time() * 1000)}"

            self._send_raw_message(f"~m~40~m~{{\"m\":\"set_auth_token\",\"p\":[\"unauthorized\"]}}")
            self._send_raw_message(f"~m~40~m~{{\"m\":\"set_locale\",\"p\":[\"en\"]}}")

            self._construct_message(session_id, chart_session, symbol, interval, n_bars)

            raw_data = ""
            max_wait = time.time() + 10

            while time.time() < max_wait:
                try:
                    result = self.ws.recv()
                    raw_data += result
                    if "series_completed" in result:
                        break
                except Exception:
                    break

            matches = re.findall(r'"s":"ok".*?"s":\[(.*?)\]', raw_data, re.DOTALL)
            if not matches:
                return None

            data_str = matches[0].replace("null", "None")
            data_list = eval(f"[{data_str}]")[0]
            if not data_list:
                return None

            df = pd.DataFrame(data_list)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)
            return df

        except Exception as e:
            print(f"Veri çekme hatası: {e}")
            return None

        finally:
            if self.ws:
                self.ws.close()
