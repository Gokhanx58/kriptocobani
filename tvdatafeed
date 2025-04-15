# tvdatafeed/main.py (Login destekli, stabilize versiyon)

import requests
import pandas as pd
from enum import Enum

class Interval(Enum):
    in_1_minute = "1"
    in_5_minute = "5"
    in_15_minute = "15"
    in_30_minute = "30"
    in_1_hour = "60"
    in_4_hour = "240"
    in_1_day = "1D"

class TvDatafeed:
    def __init__(self, session=None, session_sign=None, tv_ecuid=None):
        if not session or not session_sign or not tv_ecuid:
            raise ValueError("Tüm oturum bilgileri sağlanmalıdır (session, session_sign, tv_ecuid).")

        self.session = requests.Session()
        self.session.headers.update({
            "cookie": f"sessionid={session}; sessionid_sign={session_sign}; tv_ecuid={tv_ecuid};"
        })

    def get_hist(self, symbol, exchange='MEXC', interval=Interval.in_1_minute, n_bars=150):
        interval_value = interval.value if isinstance(interval, Interval) else interval

        symbol_str = f"{exchange}:{symbol.upper()}"

        payload = {
            "symbol": symbol_str,
            "resolution": interval_value,
            "from": 0,
            "to": 9999999999,
        }

        url = "https://tvd.wl.r.appspot.com/history"

        try:
            response = self.session.get(url, params=payload)
            response.raise_for_status()
            data = response.json()

            if not data or 't' not in data:
                print("Veri alınamadı veya format hatalı")
                return None

            df = pd.DataFrame({
                'datetime': pd.to_datetime(data['t'], unit='s'),
                'open': data['o'],
                'high': data['h'],
                'low': data['l'],
                'close': data['c'],
                'volume': data['v']
            })
            df.set_index('datetime', inplace=True)
            return df.tail(n_bars)

        except Exception as e:
            print(f"Veri alma hatası: {e}")
            return None
