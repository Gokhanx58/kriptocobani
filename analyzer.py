from tvdatafeed import TvDatafeed, Interval
from config import SYMBOLS, INTERVALS
from send_message import send_signal_to_channel
import random


def get_signal(symbol, interval):
    # Örnek sahte sinyal üretici (gerçek analiz kodunla değiştirilecek)
    price = round(random.uniform(20000, 50000), 2)
    direction = random.choice(["AL", "SAT"])
    strength = random.choice(["", "GÜÇLÜ "])
    return strength + direction, price, price + random.uniform(-100, 100)


async def analyze_signals():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            signal, signal_price, current_price = get_signal(symbol, interval)
            await send_signal_to_channel(symbol, interval, signal, signal_price, current_price)
