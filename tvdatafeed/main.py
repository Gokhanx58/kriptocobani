from .session import TvSession
from .utils import get_interval
from .const import Interval


class TvDatafeed:
    def __init__(self, username=None, password=None):
        self.session = TvSession(username, password)

    def get_hist(self, symbol, exchange, interval: Interval, n_bars=1000):
        interval_str = interval.value
        return self.session.get_hist(
            symbol=symbol,
            exchange=exchange,
            interval=interval_str,
            n_bars=n_bars
        )
