from .const import Interval
from .tvsession import TvSession
import pandas as pd

class TvDatafeed:
    def __init__(self, username: str = None, password: str = None):
        self.session = TvSession(username, password)

    def get_hist(
        self,
        symbol: str,
        exchange: str = 'BINANCE',
        interval: Interval = Interval.in_1_minute,
        n_bars: int = 5000,
    ) -> pd.DataFrame:

        data = self.session.get_hist(
            symbol=symbol,
            exchange=exchange,
            interval=interval,
            n_bars=n_bars
        )

        return data
