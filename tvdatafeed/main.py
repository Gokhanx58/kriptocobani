from .tvsession import TvSession
from .utils import get_hist, search_symbol
from .const import Interval


class TvDatafeed:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.session = TvSession()
        if username and password:
            self.session.login(username, password)

    def get_hist(self, symbol: str, exchange: str, interval: Interval = Interval.MIN_1, n_bars: int = 500):
        return get_hist(
            symbol=symbol,
            exchange=exchange,
            interval=interval,
            n_bars=n_bars,
            session=self.session
        )

    def search_symbol(self, text: str):
        return search_symbol(text, self.session)
