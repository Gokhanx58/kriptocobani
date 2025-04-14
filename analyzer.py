from tvdatafeed import TvDatafeed, Interval
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

    tv = TvDatafeed(
        session='fm0j7ziifzup5jm6sa5h6nqf65iqcxgu',
        session_sign='v3:iz6molF7z3oCKrettxY7v1u1cSvcjCnPflkvM0Pst3E=',
        tv_ecuid='10a9a8e3-be0d-4835-b7ce-bb51e801ff9b'
    )

    df = tv.get_hist(symbol=symbol, exchange='MEXC', interval=interval, n_bars=150)
    if df is None or df.empty or len(df) < 20:
        return "Veri alınamadı."

    df['high_level'] = df['high'].rolling(window=20).max()
    df['low_level'] = df['low'].rolling(window=20).min()
    df['ob_upper'] = df['open'].rolling(window=3).max()
    df['ob_lower'] = df['close'].rolling(window=3).min()

    price = df['close'].iloc[-1]
    prev_price = df['close'].iloc[-2]
    high_level = df['high_level'].iloc[-2]
    low_level = df['low_level'].iloc[-2]
    ob_high = df['ob_upper'].iloc[-2]
    ob_low = df['ob_lower'].iloc[-2]

    tolerance = 0.002  # %0.2 tolerans

    in_order_block = (ob_low * (1 - tolerance)) <= price <= (ob_high * (1 + tolerance))

    signal = "BEKLE"

    if prev_price < high_level and price > high_level and in_order_block:
        signal = "AL"
    elif prev_price > low_level and price < low_level and in_order_block:
        signal = "SAT"

    key = f"{symbol}_{interval_str}"
    if not manual and previous_signal.get(key) == signal:
        return None

    previous_signal[key] = signal
    return signal
