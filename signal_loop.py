import asyncio
from analyzer import analyze_signals
from telegram_send import send_signal_to_channel

symbols = ["BTCUSDT", "ETHUSDT", "AVAXUSDT", "SOLUSDT", "SUIUSDT"]
intervals = ["1", "5"]
previous_signals = {}
first_run = True

async def start_signal_loop():
    global first_run
    while True:
        for symbol in symbols:
            for interval in intervals:
                try:
                    signal, price = analyze_signals(symbol, interval)
                    if signal is None:
                        print(f"⚠️ {symbol} {interval}m - Sinyal alınamadı.")
                        continue

                    key = f"{symbol}_{interval}"

                    # İlk çalıştırmada mutlaka gönder
                    if first_run or previous_signals.get(key) != signal:
                        previous_signals[key] = signal
                        print(f"📤 Gönderiliyor: {symbol} {interval}m -> {signal} / {price}")
                        await send_signal_to_channel(symbol, interval, signal, price)

                    await asyncio.sleep(3)
                except Exception as e:
                    print(f"❌ {symbol} {interval} analiz hatası: {e}")

        first_run = False
        await asyncio.sleep(180)
