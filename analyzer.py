import pandas as pd
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from ta.momentum import RSIIndicator

tv = TvDatafeed()  # nologin yöntemiyle çalışıyor

# Zaman dilimi eşlemesi
interval_map = {
    "1m": Interval.in_1_minute,
    "5m": Interval.in_5_minute
}

def get_data(symbol: str, interval: str, n_bars: int = 100):
    return tv.get_hist(symbol=symbol, exchange='MEXC', interval=interval_map[interval], n_bars=n_bars)

def rsi_swing_signal(df):
    rsi = RSIIndicator(df["close"], window=7).rsi()
    overbought = 70
    oversold = 30

    last_label = None
    last_price = None
    signal = "BEKLE"

    for i in range(1, len(rsi)):
        if rsi[i - 1] < overbought and rsi[i] >= overbought:
            label = "HH" if last_price is not None and df["high"].iloc[i] > last_price else "LH"
            last_label = label
            last_price = df["high"].iloc[i]
        elif rsi[i - 1] > oversold and rsi[i] <= oversold:
            label = "LL" if last_price is not None and df["low"].iloc[i] < last_price else "HL"
            last_label = label
            last_price = df["low"].iloc[i]

    if last_label in ["HL", "LL"]:
        signal = "AL"
    elif last_label in ["HH", "LH"]:
        signal = "SAT"

    return signal

def rmi_trend_sniper(df):
    length = 14
    pmom = 66
    nmom = 30

    close = df["close"]
    up = close.diff().clip(lower=0)
    down = -close.diff().clip(upper=0)
    avg_up = up.rolling(length).mean()
    avg_down = down.rolling(length).mean()
    rsi = 100 - (100 / (1 + avg_up / avg_down))

    mfi = ((df['high'] + df['low'] + df['close']) / 3).rolling(length).mean()  # basitleştirilmiş MFI yerine
    rmi = (rsi + mfi) / 2

    # DÖNÜŞÜMLER (HATA ENGELİ)
    rmi = pd.to_numeric(rmi, errors='coerce').fillna(0)
    ema = close.ewm(span=5, adjust=False).mean()
    ema_diff = ema.diff()

    positive = (rmi.shift(1) < pmom) & (rmi > pmom) & (rmi > nmom) & (ema_diff > 0)
    negative = (rmi < nmom) & (ema_diff < 0)

    if positive.iloc[-1]:
        return "AL"
    elif negative.iloc[-1]:
        return "SAT"
    else:
        return "BEKLE"

def analyze_signals(symbol="BTCUSDT", interval="1m"):
    df = get_data(symbol, interval)
    if df is None or df.empty:
        return "Veri alınamadı."

    rsi_signal = rsi_swing_signal(df)
    rmi_signal = rmi_trend_sniper(df)

    if rsi_signal == "AL" and rmi_signal == "AL":
        return f"{symbol} [{interval}] 🔼 **AL**\n🟢 RSI: {rsi_signal}\n🟢 RMI: {rmi_signal}"
    elif rsi_signal == "SAT" and rmi_signal == "SAT":
        return f"{symbol} [{interval}] 🔻 **SAT**\n🔴 RSI: {rsi_signal}\n🔴 RMI: {rmi_signal}"
    else:
        return f"{symbol} [{interval}] ⚠️ **BEKLE**\n📉 RSI: {rsi_signal}\n📉 RMI: {rmi_signal}"
