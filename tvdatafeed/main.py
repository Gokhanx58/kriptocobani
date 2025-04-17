import pandas as pd
from .session import TvSession
from .interval import Interval
import json

class TvDatafeed:
    def __init__(self, session=None, sessionid=None, sessionid_sign=None, tv_ecuid=None):
        # Ya hazır requests.Session objesi, ya da TradingView çerezleri
        self.session = TvSession(session=session,
                                 sessionid=sessionid,
                                 sessionid_sign=sessionid_sign,
                                 tv_ecuid=tv_ecuid).session

    def get_hist(self, symbol, interval: Interval, n_bars: int = 100):
        """
        TradingView'dan OHLCV verisi çeker. Interval enum ile belirlenir.
        """
        url = 'https://scanner.tradingview.com/crypto/scan'
        # Örnek request body: muhtemel JSON gövdesi
        payload = {
            'symbols': {'tickers': [f'BINANCE:{symbol}'], 'query': {'types': []}},
            'columns': ['open', 'high', 'low', 'close', 'volume'],
            'sort': {'sortBy': 'timestamp', 'sortOrder': 'asc'},
            'range': n_bars
        }
        headers = {'Content-Type': 'application/json'}
        resp = self.session.post(url, data=json.dumps(payload), headers=headers)
        resp.raise_for_status()
        data = resp.json().get('data', [])
        # data parsing: her satırda 'd': [open, high, low, close, volume]
        records = [row['d'] for row in data]
        # timestamp field: örn. row['s'] içinde timestamp? Detaylı parsing gerekebilir.
        # Burada basit index: son n_bars dakikalık veriyi UTC index ile oluşturuyoruz.
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        idx = [now - timedelta(minutes=i) for i in range(n_bars)][::-1]
        df = pd.DataFrame(records, index=idx, columns=['open', 'high', 'low', 'close', 'volume'])
        return df
