from .main import TvDatafeed
from .interval import Interval

# tvdatafeed/interval.py
from enum import Enum

class Interval(Enum):
    MIN_1 = "1m"
    MIN_5 = "5m"

# tvdatafeed/session.py
import requests

class TvSession:
    def __init__(self, username=None, password=None, session=None, session_signature=None):
        if session and session_signature:
            self.session = requests.Session()
            # Opera TradingView cookies
            self.session.cookies.update({
                "sessionid": session,
                "sessionid_sig": session_signature
            })
        elif username and password:
            login_url = "https://www.tradingview.com/accounts/signin/"
            headers = {
                "Referer": "https://www.tradingview.com",
                "User-Agent": "Mozilla/5.0"
            }
            data = {"username": username, "password": password}
            resp = requests.post(login_url, json=data, headers=headers)
            if resp.status_code != 200:
                raise Exception(f"Giriş başarısız. Kod: {resp.status_code}")
            self.session = requests.Session()
            self.session.headers.update(headers)
            self.session.cookies.update(resp.cookies)
        else:
            raise ValueError("Username/password veya session bilgileri gerekli!")
