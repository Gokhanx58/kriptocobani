from signal_generator import generate_signals
from config import SYMBOLS, INTERVALS
from send_message import send_signal_to_channel
from tvdatafeed import TvDatafeed, Interval
import pandas as pd

# Sinyal geçmişi
last_signals = {}

# TradingView verisi çekme fonksiyonu
def get_ohlcv(symbol, interval):
    tv = TvDatafeed()
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
            if not signal_data:
                signal = "BEKLE"
            else:
                signal = signal_data[-1][1]  # En son sinyali al

            key = f"{symbol}_{interval}"

            if key not in last_signals:
                await send_signal_to_channel(symbol, interval, signal)
            elif last_signals[key] != signal:
                await send_signal_to_channel(symbol, interval, signal)

            last_signals[key] = signal
