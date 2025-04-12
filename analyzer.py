# analyzer.py

from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import numpy as np

tv = TvDatafeed()

def get_interval(interval_str):
    return {
        "1": Interval.in_1_minute,
        "5": Interval.in_5_minute,
    }.get(interval_str, Interval.in_1_minute)

def rsi_swing(df):
    rsi = ta_rsi(df['close'], 7)
    highs = df['high']
    lows = df['low']
    
    swing = []
    last_state = None
    last_price = None

    for i in range(len(rsi)):
        if rsi[i] >= 70:
            if last_state == "oversold":
                label = "AL" if lows[i] > last_price else "BEKLE"
                swing.append(label)
            else:
                swing.append("BEKLE")
            last_state = "overbought"
            last_price = highs[i]
        elif rsi[i] <= 30:
            if last_state == "overbought":
                label = "SAT" if highs[i] < last_price else "BEKLE"
                swing.append(label)
            else:
                swing.append("BEKLE")
            last_state = "oversold"
            last_price = lows[i]
        else:
            swing.append("BEKLE")

    return swing[-1]

def rmi_trend_sniper(df):
    length = 14
    pmom = 66
    nmom = 30

    change = df['close'].diff()
    up = change.clip(lower=0).rolling(length).mean()
    down = -change.clip(upper=0).rolling(length).mean()
    rsi = 100 - (100 / (1 + up / down))
    mfi = money_flow_index(df, length)
    rmi = (rsi + mfi) / 2

    ema5 = df['close'].ewm(span=5).mean()
    prev_rmi = rmi.shift(1)

    buy = (prev_rmi < pmom) & (rmi > pmom) & (rmi > nmom) & (ema5.diff() > 0)
    sell = (rmi < nmom) & (ema5.diff() < 0)

    if buy.iloc[-1]:
        return "AL"
    elif sell.iloc[-1]:
        return "SAT"
    else:
        return "BEKLE"

def analyze_signals(symbol, interval):
    try:
        df = tv.get_hist(symbol=symbol, exchange='BINANCE', interval=get_interval(interval), n_bars=100)
        if df is None or df.empty:
            return None

        rsi_result = rsi_swing(df)
        rmi_result = rmi_trend_sniper(df)

        if rsi_result == "AL" and rmi_result == "AL":
            return "AL"
        elif rsi_result == "SAT" and rmi_result == "SAT":
            return "SAT"
        else:
            return "BEKLE"

    except Exception as e:
        print(f"analyze_signals HATA: {e}")
        return None


# Yardımcı fonksiyonlar
def ta_rsi(series, period):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=(period - 1), min_periods=period).mean()
    avg_loss = loss.ewm(com=(period - 1), min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def money_flow_index(df, period):
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    money_flow = typical_price * df['volume']
    pos_flow = []
    neg_flow = []

    for i in range(1, len(typical_price)):
        if typical_price[i] > typical_price[i - 1]:
            pos_flow.append(money_flow[i])
            neg_flow.append(0)
        else:
            pos_flow.append(0)
            neg_flow.append(money_flow[i])

    pos_mf = pd.Series(pos_flow).rolling(window=period).sum()
    neg_mf = pd.Series(neg_flow).rolling(window=period).sum()
    mfi = 100 * (pos_mf / (pos_mf + neg_mf))
    mfi = mfi.reindex(df.index, method='pad')
    return mfi
