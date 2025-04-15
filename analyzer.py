from tvdatafeed import TvDatafeed, Interval
import pandas as pd

previous_signal = {}

def get_tv_interval(interval_str):
    return {
        "1": Interval.in_1_minute,
        "5": Interval.in_5_minute
    }.get(interval_str)

def analyze_signals(symbol, interval_str):
    interval = get_tv_interval(interval_str)
    if interval is None:
        return None, None

    tv = TvDatafeed(
        session='fm0j7ziifzup5jm6sa5h6nqf65iqcxgu',
        session_sign='v3:iz6molF7z3oCKrettxY7v1u1cSvcjCnPflkvM0Pst3E=',
        tv_ecuid='10a9a8e3-be0d-4835-b7ce-bb51e801ff9b'
    )

    df = tv.get_hist(symbol=symbol, exchange="MEXC", interval=interval, n_bars=150)
    if df is None or df.empty or len(df) < 20:
        return None, None

    df['high_level'] = df['high'].rolling(20).max()
    df['low_level'] = df['low'].rolling(20).min()
    df['ob_upper'] = df['open'].rolling(3).max()
    df['ob_lower'] = df['close'].rolling(3).min()

    price = df['close'].iloc[-1]
    prev_price = df['close'].iloc[-2]
    high = df['high_level'].iloc[-2]
    low = df['low_level'].iloc[-2]
    ob_high = df['ob_upper'].iloc[-2]
    ob_low = df['ob_lower'].iloc[-2]

    in_order_block = (ob_low * 0.998) <= price <= (ob_high * 1.002)
    signal = "BEKLE"
    confidence = "Normal"

    if prev_price < high and price > high and in_order_block:
        confidence = "Güçlü AL" if (price - high) / price > 0.001 else "AL"
    elif prev_price > low and price < low and in_order_block:
        confidence = "Güçlü SAT" if (low - price) / price > 0.001 else "SAT"
    else:
        return None, price

    return confidence, price
