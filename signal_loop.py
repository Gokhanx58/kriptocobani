# signal_loop.py (Güncel - Log destekli)

import asyncio
from analyzer import analyze_signals
from telegram_send import send_signal_to_channel

symbols = ["BTCUSDT", "ETHUSDT", "AVAXUSDT", "SOLUSDT", "SUIUSDT"]
intervals = ["1", "5"]
previous_signals = {}

async def start_signal_loop():
    while True:
        for symbol in symbols:
            for interval in intervals:
                try:
                    result = analyze_signals(symbol, interval, manual=False)
                    print(f"\U0001F50D {symbol} {interval}m sonucu: {result}")
                    key = f"{symbol}_{interval}"

                    if result and result != previous_signals.get(key):
                        previous_signals[key] = result
                        await send_signal_to_channel(symbol, interval, result)

                    await asyncio.sleep(3)
                except Exception as e:
                    print(f"❌ {symbol} {interval} analiz hatası: {e}")

        await asyncio.sleep(180)  # 3 dakika bekle
