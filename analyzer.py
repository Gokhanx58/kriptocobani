from tvdatafeed import TvDatafeed, Interval
from config import SYMBOLS, INTERVALS
from send_message import send_signal_to_channel
import random

# tvdatafeed ile login
tv = TvDatafeed(username="marsticaret1", password="8690Yn678690")

def get_signal(symbol, interval):
    try:
        df = tv.get_hist(symbol=symbol, exchange='MEXC', interval=Interval(interval), n_bars=300)
        if df is None or df.empty:
            print(f"⚠️ Veri alınamadı: {symbol} - {interval}")
            return None, None, None

        # Fiyat verileri doğru sütunlardan çekiliyor
        signal_price = float(df.iloc[-2]["close"])  # sinyal geldiği bar
        current_price = float(df.iloc[-1]["close"])  # son fiyat
        direction = random.choice(["AL", "SAT"])
        strength = random.choice(["", "GÜÇLÜ "])
        return strength + direction, signal_price, current_price

    except Exception as e:
        print(f"❌ Sinyal analiz hatası: {symbol} - {interval} | Hata: {e}")
        return None, None, None

async def analyze_signals():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            signal, signal_price, current_price = get_signal(symbol, interval)
            if signal and signal_price and current_price:
                await send_signal_to_channel(symbol, interval, signal, signal_price, current_price)
