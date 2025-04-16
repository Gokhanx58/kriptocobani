from signal_generator import generate_signals
from config import SYMBOLS, INTERVALS
from send_message import send_signal_to_channel
from tvdatafeed import TvDatafeed, Interval
import pandas as pd

last_signals = {}

def get_ohlcv(symbol, interval):
    tv = TvDatafeed(username="marsticaret1", password="8690Yn678690")
    tv_interval = Interval.MIN_1 if interval == "1m" else Interval.MIN_5
    df = tv.get_hist(symbol=symbol, interval=tv_interval, n_bars=100)
    if df is None or df.empty:
        return None
    df = df.sort_index()
    return df

async def analyze_signals():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            df = get_ohlcv(symbol, interval)
            if df is None:
                continue

            signal_data = generate_signals(df)
            signal = signal_data[-1][1] if signal_data else "BEKLE"

            key = f"{symbol}_{interval}"
            if key not in last_signals or last_signals[key] != signal:
                await send_signal_to_channel(symbol, interval, signal)
            last_signals[key] = signal
