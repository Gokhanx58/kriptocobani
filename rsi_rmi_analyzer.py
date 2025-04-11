from tvDatafeed import TvDatafeed
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

tv = TvDatafeed()

def analyze_signals(symbol, interval, manual=False):
    try:
        exchange = "MEXC"
        interval_map = {
            "1": "1m",
            "5": "5m",
            "15": "15m",
            "30": "30m",
            "1h": "1h",
            "4h": "4h",
            "1d": "1d",
        }
        interval_tv = interval_map.get(interval, "1m")
        data = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval_tv, n_bars=100)

        if data is None or data.empty:
            return f"{symbol} {interval_tv} için veri alınamadı."

        df = data.copy()
        df.dropna(inplace=True)

        # RMI Trend Sniper (momentum trend)
        rsi = RSIIndicator(close=df["close"], window=14).rsi()
        ema = EMAIndicator(close=df["close"], window=5).ema_indicator()
        mom_positive = (rsi > 66) & (rsi.shift(1) < 66) & (ema.diff() > 0)
        mom_negative = (rsi < 30) & (ema.diff() < 0)

        # RSI Swing (HH, LL vs mantığı basitleştirilmiş)
        swing = "BEKLE"
        if rsi.iloc[-1] > 70 and rsi.iloc[-2] > 70 and df["close"].iloc[-1] < df["close"].iloc[-2]:
            swing = "SAT"
        elif rsi.iloc[-1] < 30 and rsi.iloc[-2] < 30 and df["close"].iloc[-1] > df["close"].iloc[-2]:
            swing = "AL"

        result = f"{symbol} ({interval_tv})\n"
        if mom_positive.iloc[-1] and swing == "AL":
            result += "📈 AL SINYALİ (İki indikatör uyumlu)"
        elif mom_negative.iloc[-1] and swing == "SAT":
            result += "📉 SAT SINYALİ (İki indikatör uyumlu)"
        elif mom_positive.iloc[-1]:
            result += "RMI AL verdi ama RSI beklemede"
        elif mom_negative.iloc[-1]:
            result += "RMI SAT verdi ama RSI beklemede"
        elif swing == "AL":
            result += "RSI AL verdi ama RMI beklemede"
        elif swing == "SAT":
            result += "RSI SAT verdi ama RMI beklemede"
        else:
            result += "🔄 BEKLE sinyali"

        return result

    except Exception as e:
        return f"Hata: {str(e)}"
