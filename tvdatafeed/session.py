import requests
import pandas as pd


class TvSession:
    def __init__(self, username=None, password=None):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json",
        }

        if username and password:
            self.login(username, password)

    def login(self, username, password):
        login_url = "https://www.tradingview.com/accounts/signin/"
        payload = {
            "username": username,
            "password": password
        }

        response = self.session.post(login_url, json=payload, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Giriş başarısız. Kod: {response.status_code}, Hata: {response.text}")

    def get_hist(self, symbol, exchange, interval, n_bars=1000):
        # TradingView API endpoint burada örnek amaçlıdır, gerçekte scraping yapılır.
        # Aşağıdaki sadece format simülasyonudur.
        url = f"https://fake.tradingview.api/hist/{symbol}?exchange={exchange}&interval={interval}&n={n_bars}"

        response = self.session.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Veri çekilemedi")

        data = response.json()
        df = pd.DataFrame(data)
        return df
