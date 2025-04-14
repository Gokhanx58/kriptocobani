from tvDatafeed import TvDatafeed, Interval
import pandas as pd

previous_signal = {}

def get_tv_interval(interval_str):
    mapping = {
        "1": Interval.in_1_minute,
        "5": Interval.in_5_minute,
    }
    return mapping.get(interval_str, None)

def analyze_signals(symbol, interval_str, manual=False):
    interval = get_tv_interval(interval_str)
    if interval is None:
        return "Geçersiz zaman dilimi. Sadece 1 veya 5 dakika destekleniyor."

    tv = TvDatafeed()
    df = tv.get_hist(symbol=symbol, exchange='MEXC', interval=interval, n_bars=200)

    if df is None or df.empty or len(df) < 20:
        return "Veri alınamadı."

    df['high_level'] = df['high'].rolling(window=20).max()
    df['low_level'] = df['low'].rolling(window=20).min()

    price = df['close'].iloc[-1]
    prev_price = df['close'].iloc[-2]
    high_level = df['high_level'].iloc[-2]
    low_level = df['low_level'].iloc[-2]

    signal = "BEKLE"
    if prev_price < high_level and price > high_level:
        signal = "AL"
    elif prev_price > low_level and price < low_level:
        signal = "SAT"

    key = f"{symbol}_{interval_str}"
    if not manual and previous_signal.get(key) == signal:
        return None

    previous_signal[key] = signal
    return signal
