import asyncio
from analyzer import analyze_signals
from telegram_send import send_signal_to_channel

symbols = ["BTCUSDT", "ETHUSDT", "AVAXUSDT", "SOLUSDT", "SUIUSDT"]
intervals = ["1", "5"]
previous_signals = {}

async def start_signal_loop():
    print("⏳ Sinyal döngüsü çalışıyor...")
    for symbol in symbols:
        for interval in intervals:
            try:
                result, price = analyze_signals(symbol, interval)
                if result:
                    key = f"{symbol}_{interval}"
                    previous_signals[key] = result
                    await send_signal_to_channel(symbol, interval, result, price)
                    await asyncio.sleep(3)
            except Exception as e:
                print(f"❌ {symbol} {interval} analiz hatası: {e}")

    while True:
        for symbol in symbols:
            for interval in intervals:
                try:
                    result, price = analyze_signals(symbol, interval)
                    if result:
                        key = f"{symbol}_{interval}"
                        if previous_signals.get(key) != result:
                            previous_signals[key] = result
                            await send_signal_to_channel(symbol, interval, result, price)
                            await asyncio.sleep(3)
                except Exception as e:
                    print(f"❌ {symbol} {interval} analiz hatası: {e}")
        await asyncio.sleep(180)
