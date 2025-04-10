from tvDatafeed import TvDatafeed
import pandas as pd
from ta.momentum import RSIIndicator
import numpy as np

tv = TvDatafeed()  # nologin yöntemi

def analyze_signals(symbol, exchange, interval):
    try:
        df = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval, n_bars=200)
        if df is None or df.empty:
            return "Veri alınamadı."

        df = df.dropna()

        # RSI SWING mantığı (HL, HH, LL, LH)
        rsi = RSIIndicator(close=df["close"], window=7).rsi()
        df["rsi"] = rsi
        df["overbought"] = df["rsi"] >= 70
        df["oversold"] = df["rsi"] <= 30

        last_state = None
        swing_result = "BEKLE"

        for i in range(1, len(df)):
            if df["oversold"].iloc[i-1] and df["overbought"].iloc[i]:
                swing_result = "SAT"
                last_state = "oversold→overbought"
            elif df["overbought"].iloc[i-1] and df["oversold"].iloc[i]:
                swing_result = "AL"
                last_state = "overbought→oversold"

        # RMI Trend Sniper mantığı
        df["delta"] = df["close"].diff()
        df["gain"] = np.where(df["delta"] > 0, df["delta"], 0)
        df["loss"] = np.where(df["delta"] < 0, -df["delta"], 0)
        avg_gain = df["gain"].rolling(window=14).mean()
        avg_loss = df["loss"].rolling(window=14).mean()
        rsi_calc = 100 - (100 / (1 + avg_gain / avg_loss))
        mfi = rsi_calc  # Ortalama RSI gibi davranır
        rmi_mfi = (rsi_calc + mfi) / 2

        df["rmi_mfi"] = rmi_mfi
        df["rmi_buy"] = (df["rmi_mfi"].shift(1) < 66) & (df["rmi_mfi"] > 66)
        df["rmi_sell"] = df["rmi_mfi"] < 30

        rmi_result = "BEKLE"
        if df["rmi_buy"].iloc[-1]:
            rmi_result = "AL"
        elif df["rmi_sell"].iloc[-1]:
            rmi_result = "SAT"

        # Final sonuç
        if swing_result == rmi_result and swing_result != "BEKLE":
            return f"📢 **GÜÇLÜ {swing_result}** — Her iki indikatör aynı sinyali verdi."
        elif swing_result != rmi_result and "BEKLE" not in (swing_result, rmi_result):
            return f"⚠️ ÇAKIŞMA: RSI Swing {swing_result}, RMI {rmi_result} — Beklemede kal."
        elif swing_result != "BEKLE":
            return f"🟡 RSI Swing: {swing_result}, RMI: BEKLE — Diğeri aynı yönde sinyal verirse işlem alınabilir."
        elif rmi_result != "BEKLE":
            return f"🟡 RMI: {rmi_result}, RSI Swing: BEKLE — Diğeri aynı yönde sinyal verirse işlem alınabilir."
        else:
            return "🔍 Henüz net bir sinyal yok (BEKLE)."

    except Exception as e:
        return f"Hata oluştu: {e}"

def auto_check_signals(symbol, exchange, interval):
    result = analyze_signals(symbol, exchange, interval)
    if "GÜÇLÜ AL" in result or "GÜÇLÜ SAT" in result:
        return result
    return None
