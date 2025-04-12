# signal_loop.py

import asyncio
from analyzer import analyze_signals
from telegram_send import send_signal_to_channel

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]
intervals = ["1", "5"]
last_sent_signals = {}

async def start_signal_loop():
    while True:
        try:
            for symbol in symbols:
                for interval in intervals:
                    key = f"{symbol}_{interval}"
                    result = await analyze_signals(symbol, interval)
                    if result and result != last_sent_signals.get(key):
                        await send_signal_to_channel(result)
                        last_sent_signals[key] = result
                    await asyncio.sleep(3)
        except Exception as e:
            print(f"Hata oluştu: {e}")
        await asyncio.sleep(30)
