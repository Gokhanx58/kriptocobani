# tvdatafeed/main.py (login destekli versiyon)

import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import re
import time
import logging


class Interval:
    in_1_minute = '1'
    in_5_minute = '5'
    in_15_minute = '15'
    in_30_minute = '30'
    in_1_hour = '60'
    in_4_hour = '240'
    in_1_day = '1D'


class TvDatafeed:
    def __init__(self, username=None, password=None, session=None, session_sign=None, tv_ecuid=None):
        self.username = username
        self.password = password
        self.headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        self.session = requests.session()
        self.session.headers.update(self.headers)

        if session and session_sign and tv_ecuid:
            self.session.cookies.set('sessionid', session)
            self.session.cookies.set('sessionid_sign', session_sign)
            self.session.cookies.set('tv_ecuid', tv_ecuid)
        elif username and password:
            self.login()
        else:
            logging.warning("you are using nologin method, data you access may be limited")

    def login(self):
        login_url = 'https://www.tradingview.com/accounts/signin/'
        payload = {
            'username': self.username,
            'password': self.password,
            'remember': 'on'
        }
        response = self.session.post(login_url, json=payload)
        if response.status_code != 200:
            raise Exception('Login failed')

    def get_hist(self, symbol, exchange='BINANCE', interval=Interval.in_1_minute, n_bars=200):
        query = {
            "symbols": {
                "tickers": [f"{exchange}:{symbol}"],
                "query": {"types": []}
            },
            "columns": [
                "open", "high", "low", "close", "volume", "value",
                "is_real_time"
            ]
        }
        resp = self.session.post('https://scanner.tradingview.com/crypto/scan', json=query)
        if resp.status_code != 200:
            raise Exception('Symbol lookup failed')

        symbol_info = resp.json()['data'][0]['s'] if resp.json()['data'] else None
        if not symbol_info:
            raise Exception(f'Symbol {symbol} not found')

        symbol = f"{exchange}:{symbol}"

        payload = json.dumps({
            "symbol": symbol,
            "resolution": interval,
            "from": int((datetime.now() - timedelta(minutes=int(n_bars) * 5)).timestamp()),
            "to": int(datetime.now().timestamp()),
            "countback": n_bars,
            "currencyCode": "USD"
        })

        url = f"https://tvdce.tradingview.com/history"
        headers = self.session.headers.copy()
        headers.update({
            'Content-Type': 'application/json',
            'Referer': f'https://www.tradingview.com/chart/'
        })

        r = self.session.post(url, headers=headers, data=payload)
        if r.status_code != 200:
            raise Exception('Data fetch failed')

        data = r.json()
        if 's' in data and data['s'] != 'ok':
            raise Exception(f"TV response error: {data['s']}")

        df = pd.DataFrame(data)
        df['datetime'] = pd.to_datetime(df['t'], unit='s')
        df.set_index('datetime', inplace=True)
        df = df[['o', 'h', 'l', 'c', 'v']]
        df.columns = ['open', 'high', 'low', 'close', 'volume']
        return df
