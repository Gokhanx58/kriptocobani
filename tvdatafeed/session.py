class TvSession:
    def __init__(self, username=None, password=None, session=None, session_signature=None):
        if not username and not session:
            raise ValueError("Username/password veya session bilgisi gerekli!")
        self.username = username
        self.password = password
