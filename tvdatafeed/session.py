import requests

class TvSession:
    def __init__(self, sessionid=None, session_signature=None, tv_ecuid=None, session=None):
        if session:
            self.session = session
        else:
            # Gerekli çerez bilgileri sağlanmalı
            if not all([sessionid, session_signature, tv_ecuid]):
                raise ValueError("sessionid, session_signature ve tv_ecuid gerekli!")
            s = requests.Session()
            # TradingView headerları
            s.headers.update({
                "User-Agent": "Mozilla/5.0",
                "Referer": "https://www.tradingview.com"
            })
            # Çerezleri ayarla
            s.cookies.set('sessionid', sessionid, domain=".tradingview.com")
            s.cookies.set('session_signature', session_signature, domain=".tradingview.com")
            s.cookies.set('tv_ecuid', tv_ecuid, domain=".tradingview.com")
            self.session = s
