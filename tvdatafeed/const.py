# tvdatafeed/const.py

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/117.0.0.0 Safari/537.36"
)

TRADINGVIEW_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.tradingview.com/",
    "Origin": "https://www.tradingview.com",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
}
