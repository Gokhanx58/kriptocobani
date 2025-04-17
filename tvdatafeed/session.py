import requests

class TvSession:
    def __init__(self, username=None, password=None, session=None, session_signature=None):
        # Eğer doğrudan requests.Session nesnesi gönderilmediyse,
        # username & password kullanarak TradingView'a giriş yapar.
        if session:
            self.session = session
        elif username and password:
            self.session = self.login(username, password, session_signature)
        else:
            raise ValueError("Username/password veya session bilgisi gerekli!")
        self.username = username
        self.password = password

    def login(self, username, password, session_signature=None):
        login_url = "https://www.tradingview.com/accounts/signin/"
        headers = {
            "Referer": "https://www.tradingview.com",
            "User-Agent": "Mozilla/5.0"
        }
        payload = {
            "username": username,
            "password": password
        }
        # Eğer Opera/Chrome cookie'larınızı biliyorsanız, session_signature'ı da ekleyebilirsiniz:
        if session_signature:
            payload["session_signature"] = session_signature

        response = requests.post(login_url, json=payload, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Giriş başarısız. Kod: {response.status_code}")

        # Çerezleri yeni bir Session nesnesine aktar
        sess = requests.Session()
        sess.headers.update(headers)
        sess.cookies.update(response.cookies)
        return sess
