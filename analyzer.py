from tvdatafeed import TvDatafeed, Interval
from config import SYMBOLS, INTERVALS
from send_message import send_signal_to_channel

# Sinyal geçmişini tutan sözlük
last_signals = {}

def get_signal(symbol, interval):
    # Gerçek analiz yerine örnek (senin analiz fonksiyonunla değiştirilecek)
    import random
    return random.choice(["AL", "SAT", "BEKLE"])

async def analyze_signals():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            new_signal = get_signal(symbol, interval)
            key = f"{symbol}_{interval}"

            if key not in last_signals:
                # İlk çalıştırmada sinyali gönder
                await send_signal_to_channel(symbol, interval, new_signal)
            elif last_signals[key] != new_signal:
                # Sinyal değiştiyse gönder
                await send_signal_to_channel(symbol, interval, new_signal)

            # Güncel sinyali sakla
            last_signals[key] = new_signal
