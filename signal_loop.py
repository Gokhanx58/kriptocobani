# signal_loop.py (Güncel - İlk çalıştırmada sinyal gönderimi + fiyat bilgisi destekli)

import asyncio
from analyzer import analyze_signals
from telegram_send import send_signal_to_channel

symbols = ["BTCUSDT", "ETHUSDT", "AVAXUSDT", "SOLUSDT", "SUIUSDT"]
intervals = ["1", "5"]
previous_signals = {}
first_run = True  # İlk çalıştırma tetikleyicisi

async def start_signal_loop():
    global first_run
    print("⏳ Sinyal döngüsü başlatıldı...")
    
    while True:
        for symbol in symbols:
            for interval in intervals:
                try:
                    result, price = analyze_signals(symbol, interval, manual=False)
                    if result is None:
                        continue

                    key = f"{symbol}_{interval}"

                    if first_run or previous_signals.get(key) != result:
                        previous_signals[key] = result
                        print(f"[SİNYAL] {symbol} {interval}m → {result} @ {price:.4f}")
                        await send_signal_to_channel(symbol, interval, result, price)

                    await asyncio.sleep(3)

                except Exception as e:
                    print(f"❌ {symbol} {interval} analiz hatası: {e}")

        first_run = False
        await asyncio.sleep(180)  # 3 dakikada bir tarama
