from tvDatafeed import TvDatafeed, Interval

# TradingView kullanıcı adı ve şifrenizi buraya ekleyin
TV_USERNAME = 'marsticaret1'
TV_PASSWORD = '8690Yn678690'

# TvDatafeed'e giriş yap
tv = TvDatafeed(username=TV_USERNAME, password=TV_PASSWORD)

# Interval eşleştirmeleri
INTERVAL_MAPPING = {
    '1': Interval.in_1_minute,
    '3': Interval.in_3_minute,
    '5': Interval.in_5_minute,
    '15': Interval.in_15_minute,
    '30': Interval.in_30_minute,
    '60': Interval.in_1_hour,
    '120': Interval.in_2_hour,
    '240': Interval.in_4_hour,
    'D': Interval.in_daily,
    'W': Interval.in_weekly,
    'M': Interval.in_monthly
}

def analyze_symbol(symbol: str, interval: str) -> str:
    if interval not in INTERVAL_MAPPING:
        return 'Geçersiz zaman dilimi. Lütfen doğru bir zaman dilimi girin.'
    data = tv.get_hist(symbol=symbol, exchange='MEXC', interval=INTERVAL_MAPPING[interval], n_bars=100)
    if data is None or data.empty:
        return f'{symbol} için veri alınamadı.'
    # Burada RMI ve RSI Swing indikatörlerine göre analiz yapılacak
    # Örnek olarak basit bir hareketli ortalama kontrolü yapalım
    short_ma = data['close'].rolling(window=10).mean().iloc[-1]
    long_ma = data['close'].rolling(window=50).mean().iloc[-1]
    if short_ma > long_ma:
        return f'{symbol} {interval} zaman diliminde AL sinyali veriyor.'
    else:
        return f'{symbol} {interval} zaman diliminde SAT sinyali veriyor.'
