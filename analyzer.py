# analyzer.py

import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from tvDatafeed import TvDatafeed

tv = TvDatafeed()

def get_data(symbol, interval, n_bars=100):
    df = tv.get_hist(symbol=symbol, exchange='BINANCE', interval=interval, n_bars=n_bars)
    df = df.dropna()
    df.rename(columns={"close": "Close"}, inplace=True)
    return df

def calculate_rsi_swing(df):
    rsi = RSIIndicator(close=df["Close"], window=7).rsi()
    df["RSI"] = rsi
    df["sinyal"] = ""

    for i in range(1, len(df)):
        if df["RSI"].iloc[i - 1] < 30 and df["RSI"].iloc[i] > 30:
            df["sinyal"].iloc[i] = "HL"
        elif df["RSI"].iloc[i - 1] > 70 and df["RSI"].iloc[i] < 70:
            df["sinyal"].iloc[i] = "LH"

    son_sinyal = df["sinyal"].iloc[-1]
    if son_sinyal == "HL":
        return "AL"
    elif son_sinyal == "LH":
        return "SAT"
    else:
        return "BEKLE"

def calculate_rmi_trend_sniper(df):
    rsi = RSIIndicator(close=df["Close"], window=14).rsi()
    ema14 = df["Close"].ewm(span=14, adjust=False).mean()
    ema28 = df["Close"].ewm(span=28, adjust=False).mean()
    ema_diff = ema14 - ema28

    rmi = rsi  # Yalınlaştırılmış hali
    positive = (rmi.shift(1) < 66) & (rmi > 66) & (rmi > 30) & (ema_diff > 0)
    negative = (rmi < 30) & (ema_diff < 0)

    if positive.iloc[-1]:
        return "AL"
    elif negative.iloc[-1]:
        return "SAT"
    else:
        return "BEKLE"

async def analyze_signals(symbol: str, interval: str):
    try:
        df = get_data(symbol, interval)
        rsi_result = calculate_rsi_swing(df)
        rmi_result = calculate_rmi_trend_sniper(df)

        if rsi_result == rmi_result:
            final_signal = rsi_result
        else:
            final_signal = "BEKLE"

        return final_signal, rsi_result, rmi_result

    except Exception as e:
        print(f"[analyzer] Hata: {e}")
        return "BEKLE", "BEKLE", "BEKLE"
