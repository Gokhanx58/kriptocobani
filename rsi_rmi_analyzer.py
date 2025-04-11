from tvDatafeed import TvDatafeed
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
import logging

tv = TvDatafeed()

def get_data(symbol, interval):
    try:
        data = tv.get_hist(symbol=symbol, exchange='MEXC', interval=interval, n_bars=100)
        data = data.reset_index()
        return data
    except Exception as e:
        logging.error(f"Veri alınamadı: {e}")
        return None

def calculate_rsi_swing(data):
    rsi = RSIIndicator(close=data["close"], window=14).rsi()
    data["rsi"] = rsi
    signals = []

    for i in range(2, len(data)):
        if data["rsi"].iloc[i - 2] < 30 and data["rsi"].iloc[i - 1] > data["rsi"].iloc[i - 2] and data["rsi"].iloc[i] > data["rsi"].iloc[i - 1]:
            signals.append("HL")  # Higher Low - Potansiyel AL
        elif data["rsi"].iloc[i - 2] > 70 and data["rsi"].iloc[i - 1] < data["rsi"].iloc[i - 2] and data["rsi"].iloc[i] < data["rsi"].iloc[i - 1]:
            signals.append("LH")  # Lower High - Potansiyel SAT
        else:
            signals.append("")

    signals = [""] * 2 + signals
    data["rsi_signal"] = signals
    return data

def calculate_rmi(data):
    # Basit momentum yapısı
    delta = data["close"].diff()
    rmi = delta.rolling(window=14).mean()
    data["rmi"] = rmi
    data["rmi_signal"] = ["AL" if r > 0 else "SAT" for r in rmi]
    return data

def analyze_signals(symbol, interval, manual=False):
    tf_map = {
        "1": "1m",
        "5": "5m",
        "15": "15m",
        "30": "30m",
        "60": "1h",
        "4H": "4h",
        "1D": "1d"
    }

    tf = tf_map.get(interval.upper(), f"{interval}m")

    df = get_data(symbol, tf)
    if df is None:
        return "Veri alınamadı."

    df = calculate_rsi_swing(df)
    df = calculate_rmi(df)

    last_rsi_signal = df["rsi_signal"].iloc[-1]
    last_rmi_signal = df["rmi_signal"].iloc[-1]

    if manual:
        result = f"📊 RSI: {last_rsi_signal or 'BEKLE'}\n📈 RMI: {last_rmi_signal or 'BEKLE'}\n\n"
        if last_rsi_signal in ["HL", "LL"] and last_rmi_signal == "AL":
            return result + "✅ AL sinyali (ikisi de olumlu)"
        elif last_rsi_signal in ["HH", "LH"] and last_rmi_signal == "SAT":
            return result + "❌ SAT sinyali (ikisi de olumsuz)"
        else:
            return result + "🕒 BEKLE (uyumsuz sinyal)"
    else:
        if last_rsi_signal in ["HL", "LL"] and last_rmi_signal == "AL":
            return "AL"
        elif last_rsi_signal in ["HH", "LH"] and last_rmi_signal == "SAT":
            return "SAT"
        else:
            return "BEKLE"
