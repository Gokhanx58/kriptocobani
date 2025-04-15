# signal_loop.py

import asyncio
from analyzer import analyze_signals
import time

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]
intervals = [1, 5]  # 1m ve 5m

# Sinyal durumu kaydı
last_signals = {}

async def start_signal_loop():
    print("✅ Sinyal döngüsü başladı.")
    while True:
        for symbol in symbols:
            for interval in intervals:
                try:
                    print(f"🔍 Analiz ediliyor: {symbol}-{interval}m")
                    signal, signal_price, current_price = analyze_signals(symbol, interval)

                    key = f"{symbol}_{interval}"
                    prev_signal = last_signals.get(key)

                    if signal != prev_signal:
                        if prev_signal and prev_signal in ["AL", "GÜÇLÜ AL", "SAT", "GÜÇLÜ SAT"]:
                            from tvdatafeed.main import send_signal_to_channel
                            await send_signal_to_channel(symbol, interval, f"İŞLEMİ KAPAT ({prev_signal})", current_price)

                        if signal in ["AL", "GÜÇLÜ AL", "SAT", "GÜÇLÜ SAT"]:
                            from tvdatafeed.main import send_signal_to_channel
                            await send_signal_to_channel(symbol, interval, signal, signal_price, current_price)

                        last_signals[key] = signal

                except Exception as e:
                    print(f"❌ {symbol} {interval} analiz hatası: {e}")

                await asyncio.sleep(3)

        await asyncio.sleep(180)  # Her 3 dakikada bir döngü
