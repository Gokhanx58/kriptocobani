# signal_loop.py

import asyncio
from analyzer import analyze_signals
from telegram_send import send_signal_to_channel

symbols = ["BTCUSDT", "ETHUSDT", "AVAXUSDT", "SOLUSDT", "SUIUSDT"]
timeframes = ["1", "5"]

# Önceki sinyalleri tutmak için sözlük
last_signals = {}

async def kontrol_et(symbol, tf):
    key = f"{symbol}_{tf}"
    result = await analyze_signals(symbol, tf)

    if result is None:
        return

    if last_signals.get(key) != result:
        await send_signal_to_channel(symbol, tf, result)
        last_signals[key] = result

async def start_signal_loop():
    while True:
        try:
            for symbol in symbols:
                for tf in timeframes:
                    await kontrol_et(symbol, tf)
                    await asyncio.sleep(1.5)  # Çakışmayı önlemek için ufak gecikme
            await asyncio.sleep(180)  # 3 dakikalık ana döngü
        except Exception as e:
            print(f"HATA: {e}")
            await asyncio.sleep(10)
