from tvdatafeed.tvsession import TvSession
from tvdatafeed.utils import convert_to_df, Interval
from tvdatafeed.const import INTERVALS
import pandas as pd

class TvDatafeed:
    def __init__(self, username=None, password=None):
        self.session = TvSession()
        self.session.login(username, password)

    def get_hist(self, symbol, exchange='BINANCE', interval=Interval.in_1_minute, n_bars=500):
        data = self.session.get_hist(symbol, exchange, interval.value, n_bars)
        df = convert_to_df(data)
        return df
