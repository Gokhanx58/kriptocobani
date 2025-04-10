from tvDatafeed import TvDatafeed
from ta.momentum import RSIIndicator
import pandas as pd

tv = TvDatafeed()

def analyze_signals(symbol: str, timeframe: str, manual=False) -> str:
    try:
        df = tv.get_hist(symbol=symbol, exchange='BINANCE', interval=timeframe, n_bars=100)

        if df is None or df.empty:
            return f"⛔ Veri alınamadı: {symbol} ({timeframe})"

        df['rsi'] = RSIIndicator(close=df['close'], window=7).rsi()
        df['rsi_mfi'] = (df['rsi'] + df['volume'].rolling(14).mean()) / 2
        df['ema'] = df['close'].ewm(span=5).mean()

        last = df.iloc[-1]
        prev = df.iloc[-2]

        # RSI SWING sinyali
        rsi_signal = "BEKLE"
        if prev['rsi'] < 30 and last['rsi'] > 30:
            rsi_signal = "AL"
        elif prev['rsi'] > 70 and last['rsi'] < 70:
            rsi_signal = "SAT"

        # RMI Sniper sinyali
        rmi_signal = "BEKLE"
        if prev['rsi_mfi'] < 66 and last['rsi_mfi'] > 66 and last['ema'] > prev['ema']:
            rmi_signal = "AL"
        elif last['rsi_mfi'] < 30 and last['ema'] < prev['ema']:
            rmi_signal = "SAT"

        # Durum değerlendirmesi
        if rsi_signal == rmi_signal and rsi_signal != "BEKLE":
            emoji = "🟢" if rsi_signal == "AL" else "🔴"
            notify = "🔔" if not manual else ""
            return f"{notify}{emoji} {symbol} ({timeframe}) için NET {rsi_signal} sinyali ({rsi_signal} & {rmi_signal})"
        else:
            return f"🟡 {symbol} ({timeframe}) için BEKLE\n- RSI: {rsi_signal}\n- RMI: {rmi_signal}"

    except Exception as e:
        return f"⚠️ Analiz hatası: {e}"
