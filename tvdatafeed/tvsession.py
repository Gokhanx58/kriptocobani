# tvdatafeed/tvsession.py

import requests
from http.cookiejar import CookieJar

class TVSession:
    def __init__(self, username=None, password=None, proxies=None):
        self.username = username
        self.password = password
        self.proxies = proxies
        self.session = requests.session()
        self.session.cookies = CookieJar()
        self.authenticated = False

        if self.username and self.password:
            self.login()

    def login(self):
        login_url = 'https://www.tradingview.com/accounts/signin/'
        headers = {
            'Referer': 'https://www.tradingview.com/',
            'User-Agent': 'Mozilla/5.0'
        }
        payload = {
            'username': self.username,
            'password': self.password,
            'remember': 'on'
        }
        response = self.session.post(login_url, json=payload, headers=headers, proxies=self.proxies)

        if response.status_code == 200 and response.json().get('user'):
            self.authenticated = True
        else:
            raise Exception('Login failed to TradingView')

    def get(self, url, headers=None, params=None):
        return self.session.get(url, headers=headers, params=params, proxies=self.proxies)

    def post(self, url, headers=None, data=None, json=None):
        return self.session.post(url, headers=headers, data=data, json=json, proxies=self.proxies)

    def cookies_dict(self):
        return self.session.cookies.get_dict()
