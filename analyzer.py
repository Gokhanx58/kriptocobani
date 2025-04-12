# analyzer.py

import pandas as pd
import numpy as np
import ta

def rsi_swing(df, rsi_length=7, rsi_ob=70, rsi_os=30):
    df = df.copy()
    df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=rsi_length).rsi()
    df["sinyal"] = "BEKLE"

    laststate = None
    hh = ll = None
    last_label_price = None

    for i in range(len(df)):
        rsi_val = df["rsi"].iloc[i]
        high = df["high"].iloc[i]
        low = df["low"].iloc[i]

        if rsi_val >= rsi_ob:
            if laststate == "OS":
                label = "HH" if last_label_price is not None and high > last_label_price else "LH"
                df["sinyal"].iloc[i] = label
                last_label_price = high
            hh = max(hh or high, high)
            laststate = "OB"

        elif rsi_val <= rsi_os:
            if laststate == "OB":
                label = "LL" if last_label_price is not None and low < last_label_price else "HL"
                df["sinyal"].iloc[i] = label
                last_label_price = low
            ll = min(ll or low, low)
            laststate = "OS"

    son_sinyal = df["sinyal"].iloc[-1]
    if son_sinyal in ["HL", "LL"]:
        return "AL"
    elif son_sinyal in ["HH", "LH"]:
        return "SAT"
    else:
        return "BEKLE"


def rmi_trend_sniper(df, rmi_length=14, pmom=66, nmom=30):
    df = df.copy()
    close = df["close"]
    up = close.diff().clip(lower=0)
    down = -close.diff().clip(upper=0)
    ema_up = up.ewm(span=rmi_length).mean()
    ema_down = down.ewm(span=rmi_length).mean()
    rmi = 100 - (100 / (1 + ema_up / ema_down))
    rmi = (rmi + ta.volume.MFIIndicator(df["high"], df["low"], df["close"], df["volume"], window=rmi_length).money_flow_index()) / 2

    ema_5 = close.ewm(span=5).mean()
    ema_diff = ema_5.diff()

    # Not: Tarih indeksli veri olabilir, bu yüzden Timestamp uyarılarına dikkat
    try:
        positive = (rmi.shift(1) < pmom) & (rmi > pmom) & (rmi > nmom) & (ema_diff > 0)
        negative = (rmi < nmom) & (ema_diff < 0)
    except:
        return "BEKLE"

    if positive.iloc[-1]:
        return "AL"
    elif negative.iloc[-1]:
        return "SAT"
    else:
        return "BEKLE"


def analyze_signals(symbol, interval):
    from tvDatafeed import TvDatafeed, Interval
    tv = TvDatafeed()
    
    try:
        interval_map = {
            "1m": Interval.in_1_minute,
            "5m": Interval.in_5_minute
        }

        df = tv.get_hist(symbol=symbol, exchange="MEXC", interval=interval_map[interval], n_bars=200)
        if df is None or df.empty:
            return None

        rsi_result = rsi_swing(df)
        rmi_result = rmi_trend_sniper(df)

        if rsi_result == "AL" and rmi_result == "AL":
            return rsi_result, rmi_result, "AL"
        elif rsi_result == "SAT" and rmi_result == "SAT":
            return rsi_result, rmi_result, "SAT"
        else:
            return rsi_result, rmi_result, "BEKLE"

    except Exception as e:
        print(f"HATA - {symbol} - {interval} => {e}")
        return None
