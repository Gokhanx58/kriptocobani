# tvdatafeed/main.py
from .tvsession import TVSession
from .interval import Interval

class TvDatafeed:
    def __init__(self, username=None, password=None, auto_login=True):
        self.session = TVSession()
        if auto_login and username and password:
            self.session.login(username, password)

    def get_hist(self, symbol, exchange, interval=Interval.in_1_minute, n_bars=100):
        return self.session.get_hist(symbol, exchange, interval, n_bars)
