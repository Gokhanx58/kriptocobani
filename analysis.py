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
