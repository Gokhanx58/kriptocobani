import asyncio
from rsi_rmi_analyzer import analyze_signals
from telegram_send import send_signal_to_channel

# Sinyal takibi yapılacak semboller ve zaman dilimleri
symbols = ["BTCUSDT", "ETHUSDT", "AVAXUSDT", "SOLUSDT", "SUIUSDT"]
intervals = ["1", "5"]

# Önceki sinyalleri saklamak için sözlük
previous_signals = {}

# Sinyal döngüsünü başlatan asenkron fonksiyon
async def start_signal_loop():
    while True:
        for symbol in symbols:
            for interval in intervals:
                try:
                    result = await analyze_signals(symbol, interval)

                    key = f"{symbol}_{interval}"

                    if result != previous_signals.get(key):
                        previous_signals[key] = result
                        await send_signal_to_channel(symbol, interval, result)

                    await asyncio.sleep(3)  # Her sinyal arasında 3 saniye bekle (spam engeli)

                except Exception as e:
                    print(f"{symbol} {interval} analiz hatası: {e}")

        await asyncio.sleep(180)  # Tüm döngü bittiğinde 3 dakika bekle
