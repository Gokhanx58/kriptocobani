import requests
import pandas as pd
import ta

def fetch_ohlcv(symbol: str, interval: str, limit: int = 100):
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/ohlc?vs_currency=usd&days=1&interval={interval}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])
    df["close"] = pd.to_numeric(df["close"])
    return df

def analyze_pair(symbol: str, interval: str):
    df = fetch_ohlcv(symbol, interval)
    if df is None or df.empty:
        return "Veri alınamadı veya geçersiz sembol/zaman dilimi."

    # RSI
    rsi = ta.momentum.RSIIndicator(close=df["close"], window=14).rsi().iloc[-1]
    # MACD
    macd = ta.trend.MACD(close=df["close"])
    macd_diff = macd.macd_diff().iloc[-1]
    # EMA
    ema_short = ta.trend.EMAIndicator(close=df["close"], window=12).ema_indicator().iloc[-1]
    ema_long = ta.trend.EMAIndicator(close=df["close"], window=26).ema_indicator().iloc[-1]

    # Sinyal üretimi
    sinyaller = []
    if rsi < 30:
        sinyaller.append("RSI: AL")
    elif rsi > 70:
        sinyaller.append("RSI: SAT")
    else:
        sinyaller.append("RSI: BEKLE")

    if macd_diff > 0:
        sinyaller.append("MACD: AL")
    elif macd_diff < 0:
        sinyaller.append("MACD: SAT")
    else:
        sinyaller.append("MACD: BEKLE")

    if ema_short > ema_long:
        sinyaller.append("EMA: AL")
    elif ema_short < ema_long:
        sinyaller.append("EMA: SAT")
    else:
        sinyaller.append("EMA: BEKLE")

    karar = "AL" if sinyaller.count("AL") >= 2 else "SAT" if sinyaller.count("SAT") >= 2 else "BEKLE"

    mesaj = f"{symbol.upper()} / {interval} analizi\n" + "\n".join(sinyaller) + f"\nSonuç: {karar}"
    return mesaj
