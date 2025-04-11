# analyzer.py

from tvDatafeed import TvDatafeed, Interval
import pandas as pd

def get_tv_interval(interval_str):
    mapping = {
        "1": Interval.in_1_minute,
        "5": Interval.in_5_minute,
    }
    return mapping.get(interval_str, None)

def analyze_signals(symbol, interval_str, manual=True):
    interval = get_tv_interval(interval_str)
    if interval is None:
        return "Geçersiz zaman dilimi. Sadece 1 veya 5 dakika destekleniyor."

    tv = TvDatafeed()
    df = tv.get_hist(symbol=symbol, exchange='MEXC', interval=interval, n_bars=100)

    if df is None or df.empty:
        return "Veri alınamadı."

    df['rsi'] = compute_rsi(df['close'])
    df['rmi'] = compute_rmi(df['close'])

    latest_rsi = df['rsi'].iloc[-1]
    latest_rmi = df['rmi'].iloc[-1]

    rsi_signal = "AL" if latest_rsi < 30 else "SAT" if latest_rsi > 70 else "BEKLE"
    rmi_signal = "AL" if latest_rmi > df['rmi'].iloc[-2] else "SAT" if latest_rmi < df['rmi'].iloc[-2] else "BEKLE"

    if rsi_signal == rmi_signal:
        return rsi_signal
    else:
        return f"BEKLE: RSI = {rsi_signal}, RMI = {rmi_signal}"

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def compute_rmi(series, period=14, momentum=5):
    momentum_diff = series.diff(periods=momentum)
    gain = (momentum_diff.where(momentum_diff > 0, 0)).rolling(window=period).mean()
    loss = (-momentum_diff.where(momentum_diff < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
