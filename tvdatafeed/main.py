from tvdatafeed.interval import Interval
from tvdatafeed.tvsession import TvSession
import pandas as pd

class TvDatafeed:
    def __init__(self):
        self.session = TvSession()

    def get_hist(self, symbol: str, exchange: str, interval: Interval, n_bars: int = 100):
        url = f"https://api.binance.com/api/v3/klines"
        params = {
            "symbol": symbol.replace("/", "").upper(),
            "interval": interval.value,
            "limit": n_bars
        }
        data = self.session.get_data(url, params)
        if not data:
            return None

        df = pd.DataFrame(data, columns=[
            'datetime', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
        ])
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
        df.set_index('datetime', inplace=True)
        df = df.astype(float)
        return df
