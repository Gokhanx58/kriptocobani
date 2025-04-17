import pandas as pd
from .session import TvSession

class TvDatafeed:
    def __init__(self, username=None, password=None, session=None, session_signature=None):
        self.session = TvSession(username, password, session, session_signature)

    def get_hist(self, symbol, interval, n_bars=100):
        # Örnek sahte veri (test için)
        from datetime import datetime, timedelta
        import random

        now   = datetime.utcnow()
        index = [now - timedelta(minutes=i) for i in range(n_bars)][::-1]
        return pd.DataFrame({
            'open':  [random.uniform(100,110) for _ in range(n_bars)],
            'high':  [random.uniform(110,115) for _ in range(n_bars)],
            'low':   [random.uniform(95,100) for _ in range(n_bars)],
            'close': [random.uniform(100,110) for _ in range(n_bars)],
            'volume':[random.randint(100,1000) for _ in range(n_bars)],
        }, index=index)
