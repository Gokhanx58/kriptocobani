import pandas as pd
from datetime import datetime, timedelta
from .session import TvSession
from .interval import Interval

class TvDatafeed:
    """
    TvDatafeed: TradingView tarihsel veri çekicisi.
    Gerçek API olmadığı için burada örnek rasgele veri döndürüyor,
    ama session kullanımı hazır durumda.
    """
    def __init__(self,
                 sessionid: str,
                 sessionid_sign: str,
                 tv_ecuid: str):
        self.session = TvSession(sessionid, sessionid_sign, tv_ecuid).session

    def get_hist(self,
                 symbol: str,
                 interval: Interval = Interval.MIN_1,
                 n_bars: int = 100) -> pd.DataFrame:
        """
        Son n_bars kadar OHLCV verisini getirir (simülasyon).
        interval.value: '1m' veya '5m'
        """
        now = datetime.utcnow()
        # zaman dizisi
        index = [now - timedelta(minutes=i) for i in range(n_bars)][::-1]
        df = pd.DataFrame({
            'open':   pd.np.random.uniform(100, 110, size=n_bars),
            'high':   pd.np.random.uniform(110, 115, size=n_bars),
            'low':    pd.np.random.uniform(95, 100, size=n_bars),
            'close':  pd.np.random.uniform(100, 110, size=n_bars),
            'volume': pd.np.random.randint(100, 1000, size=n_bars),
        }, index=index)
        df.index.name = 'timestamp'
        return df
