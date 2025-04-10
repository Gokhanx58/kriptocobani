from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import numpy as np

tv = TvDatafeed(username='marsticaret1', password='8690Yn678690')

def analyze_symbol(symbol, timeframe):
    interval_map = {
        '1': Interval.in_1_minute,
        '5': Interval.in_5_minute,
        '15': Interval.in_15_minute,
        '30': Interval.in_30_minute,
        '60': Interval.in_1_hour,
        '240': Interval.in_4_hour,
        '1d': Interval.in_daily
    }

    interval = interval_map.get(timeframe, Interval.in_15_minute)
    data = tv.get_hist(symbol=symbol, exchange='BINANCE', interval=interval, n_bars=100)

    if data is None or data.empty:
        return f"{symbol} için veri alınamadı."

    data['rsi'] = compute_rsi(data['close'])
    data['rmi'] = compute_rmi(data['close'])

    latest_rsi = data['rsi'].iloc[-1]
    latest_rmi = data['rmi'].iloc[-1]

    if latest_rsi < 30 and latest_rmi > 50:
        return f"{symbol} ({timeframe}) için ✅ **AL** sinyali"
    elif latest_rsi > 70 and latest_rmi < 50:
        return f"{symbol} ({timeframe}) için ❌ **SAT** sinyali"
    else:
        return f"{symbol} ({timeframe}) için 📊 **NÖTR**"

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def compute_rmi(series, length=20, momentum=5):
    momentum_diff = series.diff(momentum)
    up = momentum_diff.where(momentum_diff > 0, 0)
    down = -momentum_diff.where(momentum_diff < 0, 0)
    avg_up = up.rolling(length).mean()
    avg_down = down.rolling(length).mean()
    rmi = 100 - (100 / (1 + (avg_up / avg_down)))
    return rmi
