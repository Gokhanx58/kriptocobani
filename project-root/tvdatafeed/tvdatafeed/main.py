import pandas as pd
import json
import time
import random
import logging
from typing import Optional
import websocket
import requests
import re
import datetime
import urllib.parse
import hashlib

class TvDatafeed:
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        self.username = username
        self.password = password
        self.auth_token = None

        if username and password:
            self.login()

    def login(self):
        try:
            login_url = 'https://www.tradingview.com/accounts/signin/'
            headers = {
                'Referer': 'https://www.tradingview.com'
            }
            payload = {
                'username': self.username,
                'password': self.password
            }

            response = requests.post(login_url, json=payload, headers=headers)
            if response.status_code == 200 and 'sessionid' in response.cookies:
                self.session = requests.Session()
                self.session.headers.update(headers)
                self.session.cookies.update(response.cookies)
                print("[tvdatafeed] Giriş başarılı.")
            else:
                print("[tvdatafeed] Giriş başarısız.")
        except Exception as e:
            print(f"[tvdatafeed] Giriş sırasında hata: {e}")
