import requests
import pandas as pd
import ta

def fetch_data(symbol: str, interval: str):
    gecko_map = {
        "btcusdt": "bitcoin",
        "ethusdt": "ethereum",
        "solusdt": "solana",
        "avaxusdt": "avalanche-2",
        "suiusdt": "sui"
    }

    coin_id = gecko_map.get(symbol.lower())
    if not coin_id:
        print(f"[HATA] Coin eşleşmesi bulunamadı: {symbol}")
        return None

    interval_map = {
        "1": "minutely",
        "5": "minutely",
        "15": "minutely",
        "30": "minutely",
        "60": "hourly",
        "1h": "hourly",
        "4h": "hourly",
        "1d": "daily"
    }

    cg_interval = interval_map.get(interval.lower())
    if not cg_interval:
        print(f"[HATA] Zaman dilimi eşleşmesi yok: {interval}")
        return None

    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "1",
        "interval": cg_interval
    }

    print(f"[INFO] İstek atılıyor → {url}")
    print(f"[INFO] Parametreler: {params}")

    response = requests.get(url, params=params)

    print(f"[INFO] Response status code: {response.status_code}")
    if response.status_code != 200:
        print(f"[HATA] CoinGecko response: {response.text}")
        return None

    prices = response.json().get("prices", [])
    if not prices:
        print(f"[HATA] Gelen veri boş")
        return None

    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    return df

def analyze_pair(symbol: str, interval: str):
    df = fetch_data(symbol, interval)
    if df is None or df.empty:
        return "Veri alınamadı veya geçersiz sembol/zaman dilimi."

    rsi = ta.momentum.RSIIndicator(close=df["price"], window=14).rsi().iloc[-1]
    macd = ta.trend.MACD(close=df["price"])
    macd_diff = macd.macd_diff().iloc[-1]
    ema12 = ta.trend.EMAIndicator(close=df["price"], window=12).ema_indicator().iloc[-1]
    ema26 = ta.trend.EMAIndicator(close=df["price"], window=26).ema_indicator().iloc[-1]

    sinyaller = []
    if rsi < 30:
        sinyaller.append("RSI: AL")
    elif rsi > 70:
        sinyaller.append("RSI: SAT")
    else:
        sinyaller.append("RSI: BEKLE")

    sinyaller.append("MACD: AL" if macd_diff > 0 else "MACD: SAT")
    sinyaller.append("EMA: AL" if ema12 > ema26 else "EMA: SAT")

    karar = "AL" if sinyaller.count("AL") >= 2 else "SAT" if sinyaller.count("SAT") >= 2 else "BEKLE"

    mesaj = f"{symbol.upper()} / {interval}dk ANALİZ\\n" + "\\n".join(sinyaller) + f"\\n🔔 Sonuç: {karar}"
    return mesaj
