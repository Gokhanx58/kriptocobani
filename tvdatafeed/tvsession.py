import requests

class TVSession:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Origin': 'https://www.tradingview.com'
        }

        self.cookies = {
            'sessionid': 'fm0j7ziifzup5jm6sa5h6nqf65iqcxgu',
            'sessionid_sign': 'v3:iz6molF7z3oCKrettxY7v1u1cSvcjCnPflkvM0Pst3E=',
            'tv_ecuid': '10a9a8e3-be0d-4835-b7ce-bb51e801ff9b'
        }

    def get_hist(self, symbol, exchange, interval, n_bars=500):
        url = f"https://tvd.tradingview.com/history"
        params = {
            'symbol': f"{exchange}:{symbol}",
            'resolution': interval.value,
            'from': 999999999,
            'to': 9999999999,
            'countback': n_bars
        }
        response = requests.get(url, headers=self.headers, cookies=self.cookies, params=params)
        data = response.json()
        return data
