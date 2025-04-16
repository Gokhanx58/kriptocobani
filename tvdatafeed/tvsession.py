class TvSession:
    def login(self, username=None, password=None):
        pass  # Login simülasyonu (dummy yapı)
    
    def get_hist(self, symbol, exchange, interval, n_bars):
        # Dummy verisi döndüren simülasyon
        from datetime import datetime, timedelta
        import pandas as pd
        now = datetime.now()
        data = []
        for i in range(n_bars):
            data.append({
                'datetime': now - timedelta(minutes=i),
                'open': 100 + i * 0.1,
                'high': 101 + i * 0.1,
                'low': 99 + i * 0.1,
                'close': 100 + i * 0.1,
                'volume': 1000 + i
            })
        return data
