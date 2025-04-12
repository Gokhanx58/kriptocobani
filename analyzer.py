import pandas as pd
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from datetime import datetime, timedelta

# Giriş yapılmadan (nologin) veri çekiliyor
tv = TvDatafeed()

# Önceki sinyali hafızada tutan global değişken
last_signals = {}

# RSI hesaplama
def calculate_rsi(series, length=7):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(length).mean()
    avg_loss = loss.rolling(length).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# MFI hesaplama
def calculate_mfi(df, period=14):
    tp = (df['close'] + df['high'] + df['low']) / 3
    mf = tp * df['volume']
    pos_mf = np.where(tp > tp.shift(1), mf, 0)
    neg_mf = np.where(tp < tp.shift(1), mf, 0)
    mfi = 100 * (pd.Series(pos_mf).rolling(period).sum() /
                (pd.Series(pos_mf).rolling(period).sum() + pd.Series(neg_mf).rolling(period).sum()))
    return mfi

# RMI hesaplama: RSI + MFI ortalaması
def calculate_rmi(df, period=14):
    rsi = calculate_rsi(df['close'], period)
    mfi = calculate_mfi(df, period)
    return (rsi + mfi) / 2

# RMI Sniper sinyali (momentum)
def get_rmi_sniper(df):
    rmi = calculate_rmi(df)
    ema = df['close'].ewm(span=5).mean()
    ema_diff = ema.diff()

    positive = (rmi.shift(1) < 66) & (rmi > 66) & (rmi > 30) & (ema_diff > 0)
    negative = (rmi < 30) & (ema_diff < 0)

    if positive.iloc[-1]:
        return "AL"
    elif negative.iloc[-1]:
        return "SAT"
    else:
        return "BEKLE"

# RSI Swing sinyali (trend yapısı)
def get_rsi_swing(df, rsi_len=7, overbought=70, oversold=30):
    rsi = calculate_rsi(df['close'], rsi_len)
    signal = "BEKLE"

    if rsi.iloc[-2] <= oversold and rsi.iloc[-1] > oversold:
        if df['low'].iloc[-1] > df['low'].iloc[-2]:
            signal = "AL"

    elif rsi.iloc[-2] >= overbought and rsi.iloc[-1] < overbought:
        if df['high'].iloc[-1] < df['high'].iloc[-2]:
            signal = "SAT"

    return signal

# Zaman dilimi eşleşmesi
timeframe_map = {
    "1": Interval.in_1_minute,
    "5": Interval.in_5_minute
}

# Ana analiz fonksiyonu
def analyze_signals(symbol: str, tf_str: str = "1", manual=False):
    try:
        interval = timeframe_map.get(tf_str, Interval.in_1_minute)
        df = tv.get_hist(symbol=symbol, exchange="MEXC", interval=interval, n_bars=200)
        if df is None or len(df) < 20:
            return "Veri alınamadı."

        df = df.dropna()

        rsi_signal = get_rsi_swing(df)
        rmi_signal = get_rmi_sniper(df)

        signal_key = f"{symbol}_{tf_str}"
        previous_signal = last_signals.get(signal_key, "BEKLE")
        combined_signal = "BEKLE"

        if rsi_signal == rmi_signal and rsi_signal in ["AL", "SAT"]:
            combined_signal = rsi_signal
        elif rsi_signal in ["AL", "SAT"] or rmi_signal in ["AL", "SAT"]:
            combined_signal = "BEKLE"

        # Sadece sinyal değiştiyse dön
        if not manual:
            if previous_signal != combined_signal:
                last_signals[signal_key] = combined_signal
                return f"<b>{symbol} ({tf_str}dk)</b>\n🧠 RSI Swing: {rsi_signal}\n📊 RMI Trend Sniper: {rmi_signal}\n📢 Sinyal: <b>{combined_signal}</b>"
            return None
        else:
            return f"<b>{symbol} ({tf_str}dk)</b>\n🧠 RSI Swing: {rsi_signal}\n📊 RMI Trend Sniper: {rmi_signal}\n📢 Sinyal: <b>{combined_signal}</b>"

    except Exception as e:
        return f"Hata: {str(e)}"
