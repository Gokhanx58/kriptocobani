from .session import TvSession
from .const import Interval

class TvDatafeed:
    def __init__(self):
        self.session = TvSession()

    def get_hist(self, symbol, interval, exchange="BINANCE", n_bars=200):
        return []
