from .session import TvSession
from .interval import Interval

class TvDatafeed:
    def __init__(self, sessionid=None, session_signature=None, tv_ecuid=None, session=None):
        # TvSession doğrudan mevcut session veya çerez bilgileri ile oluşturulur
        self.session = TvSession(
            sessionid=sessionid,
            session_signature=session_signature,
            tv_ecuid=tv_ecuid,
            session=session
        ).session

    def get_hist(self, symbol, interval=Interval.MIN_1, exchange="BINANCE", n_bars=200):
        # Burada TradingView REST API ya da websocket entegrasyonu olacak
        # Örneğin:
        url = f"https://api.tradingview.com/history?symbol={symbol}&resolution={interval.value}&countback={n_bars}"
        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()
        # Veriyi DataFrame'e dönüştürme
        import pandas as pd
        df = pd.DataFrame({
            'open': data['o'],
            'high': data['h'],
            'low': data['l'],
            'close': data['c'],
            'volume': data['v'],
        }, index=pd.to_datetime(data['t'], unit='s'))
        return df
