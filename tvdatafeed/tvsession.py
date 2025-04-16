import pandas as pd
import requests
from .interval import Interval

class TvDatafeed:
    def __init__(self):
        pass

    def get_hist(self, symbol, exchange, interval, n_bars=100):
        # Sahte veri (örnek/test)
        data = {
            'datetime': pd.date_range(end=pd.Timestamp.now(), periods=n_bars, freq='1min'),
            'open': [100 + i for i in range(n_bars)],
            'high': [101 + i for i in range(n_bars)],
            'low': [99 + i for i in range(n_bars)],
            'close': [100 + i for i in range(n_bars)],
            'volume': [1000 for _ in range(n_bars)],
        }
        return pd.DataFrame(data)
