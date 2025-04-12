import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from tvDatafeed import TvDatafeed

# Girişli tvdatafeed
tv = TvDatafeed(username='marsticaret1', password='8690Yn678690')

def get_data(symbol, interval, n_bars=100):
    df = tv.get_hist(symbol=symbol, exchange='BINANCE', interval=interval, n_bars=n_bars)
    df = df.dropna()
    df.rename(columns={"close": "Close"}, inplace=True)
    return df

def calculate_rsi_swing(df):
    rsi = RSIIndicator(close=df["Close"], window=7).rsi()
    df["RSI"] = rsi
    df["sinyal"] = None

    for i in range(1, len(df)):
        prev = rsi.iloc[i - 1]
        curr = rsi.iloc[i]
        label = None
        if prev < 30 and curr > 30:
            label = "HL"
        elif prev > 70 and curr < 70:
            label = "LH"
        df.loc[df.index[i], "sinyal"] = label

    last_signal = df["sinyal"].dropna().iloc[-1] if not df["sinyal"].dropna().empty else None
    if last_signal in ["HL", "LL"]:
        return "AL"
    elif last_signal in ["LH", "HH"]:
        return "SAT"
    return "BEKLE"

def calculate_rmi_trend_sniper(df):
    rsi = RSIIndicator(close=df["Close"], window=14).rsi()
    ema14 = df["Close"].ewm(span=14, adjust=False).mean()
    ema28 = df["Close"].ewm(span=28, adjust=False).mean()
    ema_diff = ema14 - ema28

    positive = (rsi.shift(1) < 66) & (rsi > 66) & (rsi > 30) & (ema_diff > 0)
    negative = (rsi < 30) & (ema_diff < 0)

    if positive.iloc[-1]:
        return "AL"
    elif negative.iloc[-1]:
        return "SAT"
    return "BEKLE"

async def analyze_signals(symbol: str, interval: str):
    try:
        df = get_data(symbol, interval)
        rsi_result = calculate_rsi_swing(df)
        rmi_result = calculate_rmi_trend_sniper(df)

        if rsi_result == rmi_result:
            final_signal = rsi_result
        elif rsi_result != "BEKLE" or rmi_result != "BEKLE":
            final_signal = "BEKLE"
        else:
            final_signal = None

        return final_signal, rsi_result, rmi_result

    except Exception as e:
        print(f"[analyzer] Hata: {e}")
        return None, "BEKLE", "BEKLE"
