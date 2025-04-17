# binance_client.py
import pandas as pd
import requests

def get_klines(symbol: str, interval: str, limit: int = 200) -> pd.DataFrame:
    """
    Binance Klines endpoint’inden OHLCV çeker.
    interval: '1m', '5m', '1h', ... limit: bar sayısı
    """
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    data = requests.get(url, params=params, timeout=10).json()
    df = pd.DataFrame(data, columns=[
        "open_time","open","high","low","close","volume","close_time",
        "quote_asset_vol","num_trades","taker_buy_base","taker_buy_quote","ignore"
    ])
    # timestamp index
    df.index = pd.to_datetime(df["close_time"], unit="ms")
    # numeric dönüşümler
    for col in ["open","high","low","close","volume"]:
        df[col] = df[col].astype(float)
    return df[["open","high","low","close","volume"]]
