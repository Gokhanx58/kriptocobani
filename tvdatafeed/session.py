import requests

class TvSession:
    def __init__(self, session=None, sessionid=None, sessionid_sign=None, tv_ecuid=None):
        # Beklenen çerez bilgileri ya da hazır session
        if session:
            self.session = session
        elif sessionid and sessionid_sign and tv_ecuid:
            self.session = self._build_session(sessionid, sessionid_sign, tv_ecuid)
        else:
            raise ValueError("TvSession: session objesi veya çerez bilgileri (sessionid, sessionid_sign, tv_ecuid) gerekli!")

    def _build_session(self, sessionid, sessionid_sign, tv_ecuid):
        s = requests.Session()
        s.cookies.set('sessionid', sessionid, domain='tradingview.com')
        s.cookies.set('sessionid_sig', sessionid_sign, domain='tradingview.com')
        s.cookies.set('tv_ecuid', tv_ecuid, domain='tradingview.com')
        s.headers.update({
            'Referer': 'https://www.tradingview.com',
            'User-Agent': 'Mozilla/5.0'
        })
        return s
