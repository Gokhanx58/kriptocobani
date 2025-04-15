import asyncio
from analyzer import analyze_signals
from telegram_send import send_signal_to_channel

symbols = ["BTCUSDT", "ETHUSDT", "AVAXUSDT", "SOLUSDT", "SUIUSDT"]
intervals = ["1", "5"]
previous_signals = {}
first_run = True

async def start_signal_loop():
    global first_run
    print("📊 Sinyal döngüsü başlatıldı.")  # DEBUG log
    while True:
        for symbol in symbols:
            for interval in intervals:
                try:
                    print(f"🔍 Analiz başlatıldı: {symbol} {interval}m")  # DEBUG log
                    signal, price = analyze_signals(symbol, interval, manual=False)
                    if signal is None or price is None:
                        continue

                    key = f"{symbol}_{interval}"
                    if first_run or previous_signals.get(key) != signal:
                        previous_signals[key] = signal
                        await send_signal_to_channel(symbol, interval, signal, price)

                    await asyncio.sleep(3)

                except Exception as e:
                    print(f"❌ {symbol} {interval} analiz hatası: {e}")

        first_run = False
        await asyncio.sleep(180)
