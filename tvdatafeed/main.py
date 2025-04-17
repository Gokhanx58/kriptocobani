from .session import TvSession
from .interval import Interval
import pandas as pd
from datetime import datetime, timedelta
import random

class TvDatafeed:
    def __init__(self, username=None, password=None, session=None, session_signature=None):
        # Yerel TvSession kullanır
        self.session = TvSession(username, password, session, session_signature)

    def get_hist(self, symbol, interval=Interval.MIN_1, n_bars=100):
        """
        Gerçek dünyada burada self.session ile TradingView API'sine istek
        atıp OHLCV çekersiniz. Şu an için demo amaçlı rastgele veri üretiyor.
        """
        now = datetime.utcnow()
        # Zaman index'i geriye doğru n_bars dakikalık
        index = [now - timedelta(minutes=i * (1 if interval == Interval.MIN_1 else 5))
                 for i in range(n_bars)][::-1]
        df = pd.DataFrame({
            'open':  [random.uniform(100, 110) for _ in range(n_bars)],
            'high':  [random.uniform(110, 115) for _ in range(n_bars)],
            'low':   [random.uniform(95, 100)   for _ in range(n_bars)],
            'close': [random.uniform(100, 110) for _ in range(n_bars)],
            'volume':[random.randint(100, 1000)for _ in range(n_bars)],
        }, index=index)
        return df
