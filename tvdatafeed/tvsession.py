import requests

class TvSession:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0"
        })

    def get_data(self, url, params=None):
        response = self.session.get(url, params=params)
        return response.json()
