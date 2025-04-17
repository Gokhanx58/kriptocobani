import pandas as pd
from datetime import datetime, timedelta
from .session import TvSession
from .interval import Interval

class TvDatafeed:
    def __init__(self, username=None, password=None, session=None, session_signature=None):
        self.session = TvSession(username, password, session, session_signature)

    def get_hist(self, symbol, interval: Interval, n_bars=200):
        # TODO: Gerçek veriyi self.session üzerinden çekin. Şu an örnek rastgele veri:
        now = datetime.utcnow()
        idx = [now - timedelta(minutes=i) for i in range(n_bars)][::-1]
        return pd.DataFrame({
            'open':  pd.np.random.uniform(100,110,n_bars),
            'high':  pd.np.random.uniform(110,115,n_bars),
            'low':   pd.np.random.uniform(95,100,n_bars),
            'close': pd.np.random.uniform(100,110,n_bars),
            'volume': pd.np.random.randint(100,1000,n_bars)
        }, index=idx)
