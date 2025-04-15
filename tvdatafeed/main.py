from .tvsession import TVSession
from .const import INTERVALS
from .utils import *
from datetime import datetime
from .interval import Interval

class TvDatafeed:
    def __init__(self, username='', password='', session=None, session_sign=None, tv_ecuid=None):
        self.username = username
        self.password = password
        self.session = TVSession(username, password, session, session_sign, tv_ecuid)

    def get_hist(self, symbol, exchange, interval=Interval.in_1_minute, n_bars=200):
        return self.session.get_hist(symbol, exchange, interval, n_bars)
