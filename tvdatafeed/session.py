import requests
import logging

class TvSession:
    def __init__(self, username=None, password=None, session=None, session_signature=None):
        self.username = username
        self.password = password

        if session:
            self.session = session
            logging.info("Mevcut oturum kullanıldı.")
        elif username and password:
            self.session = self.login(username, password)
        else:
            raise ValueError("Username/password veya session bilgisi gerekli!")

    def login(self, username, password):
        login_url = "https://www.tradingview.com/accounts/signin/"
        headers = {
            "Referer": "https://www.tradingview.com",
            "User-Agent": "Mozilla/5.0"
        }
        data = {"username": username, "password": password}

        response = requests.post(login_url, json=data, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Giriş başarısız. Kod: {response.status_code}")

        session = requests.Session()
        session.headers.update(headers)
        session.cookies.update(response.cookies)
        logging.info("TradingView oturumu başarıyla oluşturuldu.")
        return session
