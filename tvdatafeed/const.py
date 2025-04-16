INTERVALS = {
    "1m": "1",
    "5m": "5",
    "15m": "15",
    "30m": "30",
    "1h": "60",
    "4h": "240",
    "1d": "D",
    "1w": "W",
    "1M": "M"
}

SCREENER = "crypto"

GET_HISTORY_PAYLOAD = {
    "symbol": "",
    "resolution": "",
    "from": 0,
    "to": 0,
    "countback": 300,
    "currencyCode": "USD"
}

WEBSOCKET_HEADERS = {
    "Connection": "Upgrade",
    "Upgrade": "websocket",
    "Host": "prodata.tradingview.com",
    "Origin": "https://www.tradingview.com",
    "User-Agent": "Mozilla/5.0"
}
