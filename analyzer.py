from tvdatafeed import TvDatafeed, Interval
from utils import round_to_nearest
import pandas as pd

def analyze_signals(symbol, interval):
    tv = TvDatafeed()
    df = tv.get_hist(
        symbol=symbol,
        exchange='BINANCE',
        interval=Interval(interval),
        n_bars=100
    )

    if df is None or df.empty:
        return None

    # Sinyal tipi belirleme mantığı (örnek olarak trendin yönüne göre)
    last_close = df['close'].iloc[-1]
    prev_close = df['close'].iloc[-2]

    if last_close > prev_close:
        signal = 'AL'
        comment = 'Yükseliş bekleniyor'
        icon = '✅'
    elif last_close < prev_close:
        signal = 'SAT'
        comment = 'Geri çekilme bekleniyor'
        icon = '❌'
    else:
        signal = 'BEKLE'
        comment = 'Net sinyal yok'
        icon = '⏸'

    signal_price = round_to_nearest(prev_close)
    current_price = round_to_nearest(last_close)

    return {
        'signal': signal,
        'comment': comment,
        'icon': icon,
        'signal_price': signal_price,
        'current_price': current_price
    }
