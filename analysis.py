import pandas as pd
from tvDatafeed import TvDatafeed, Interval
from ta.momentum import RSIIndicator

def get_interval_str(timeframe: str) -> Interval:
    return {
        '1m': Interval.in_1_minute,
        '5m': Interval.in_5_minute,
        '15m': Interval.in_15_minute,
        '30m': Interval.in_30_minute,
        '1h': Interval.in_1_hour,
        '4h': Interval.in_4_hour,
        '1d': Interval.in_daily
    }.get(timeframe, Interval.in_5_minute)

def analyze_rmi_rsi(symbol: str, exchange: str, timeframe: str = '5m') -> str:
    tv = TvDatafeed()
    interval = get_interval_str(timeframe)
    df = tv.get_hist(symbol=symbol.upper(), exchange=exchange, interval=interval, n_bars=100)

    if df is None or df.empty:
        return "Veri alınamadı."

    # RSI Swing hesaplama
    rsi = RSIIndicator(close=df['close'], window=14).rsi()
    latest_rsi = rsi.iloc[-1]

    # RMI hesaplama (RSI'ın hareketli versiyonu gibi düşün)
    df['rmi'] = df['close'].diff(1).apply(lambda x: max(x, 0)).rolling(window=5).mean()
    df['rmi'] -= df['close'].diff(1).apply(lambda x: abs(x)).rolling(window=5).mean()
    df['rmi'] = df['rmi'].fillna(0)
    latest_rmi = df['rmi'].iloc[-1]

    if latest_rsi < 30 and latest_rmi > 0:
        return "🔼 AL"
    elif latest_rsi > 70 and latest_rmi < 0:
        return "🔻 SAT"
    else:
        return "⏳ BEKLE"

