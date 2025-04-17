import requests

class TvSession:
    """
    TradingView oturumu. Opera'dan aldığınız çerez bilgilerini kullanarak
    oturumu hazırlar. sessionid, sessionid_sign ve tv_ecuid değerlerini
    ENV değişkeni veya doğrudan buraya yazabilirsiniz.
    """
    def __init__(self,
                 sessionid: str,
                 sessionid_sign: str,
                 tv_ecuid: str):
        self.session = requests.Session()
        # TradingView çerezleri
        self.session.cookies.set('sessionid', sessionid, domain='.tradingview.com')
        self.session.cookies.set('sessionid_sig', sessionid_sign, domain='.tradingview.com')
        self.session.cookies.set('tv_ecuid', tv_ecuid, domain='.tradingview.com')
        # temel header'lar
        self.session.headers.update({
            'Referer': 'https://www.tradingview.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        })
