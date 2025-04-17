# binance_client.py
import pandas as pd
import requests
import logging

logging.basicConfig(level=logging.INFO)

def get_klines(symbol: str, interval: str, limit: int = 200) -> pd.DataFrame:
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            logging.error(f"{symbol}-{interval}: Binance HTTP {resp.status_code} → {resp.text}")
            return pd.DataFrame()
        data = resp.json()
        df = pd.DataFrame(data, columns=[
            "open_time","open","high","low","close","volume",
            "close_time","quote_asset_vol","num_trades",
            "taker_buy_base","taker_buy_quote","ignore"
        ])
        df.index = pd.to_datetime(df["close_time"], unit="ms")
        for col in ["open","high","low","close","volume"]:
            df[col] = df[col].astype(float)
        return df[["open","high","low","close","volume"]]
    except Exception as e:
        logging.error(f"{symbol}-{interval}: get_klines exception → {e}")
        return pd.DataFrame()
