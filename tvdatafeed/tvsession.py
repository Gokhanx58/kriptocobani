import requests


class TvSession:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.tradingview.com"
        }

        if self.username and self.password:
            self.login()

    def login(self):
        try:
            url = "https://www.tradingview.com/accounts/signin/"
            payload = {
                "username": self.username,
                "password": self.password,
                "remember": "on"
            }
            response = self.session.post(url, json=payload, headers=self.headers)

            if response.status_code == 200 and "sessionid" in response.cookies:
                print("✅ TradingView oturumu başarıyla başlatıldı.")
            else:
                print("❌ Giriş başarısız. Yanıt kodu:", response.status_code)
                print(response.text)

        except Exception as e:
            print(f"⚠️ Giriş sırasında hata oluştu: {e}")
