import asyncio
from rsi_rmi_analyzer import analyze_signals
from telegram_send import send_signal_to_channel

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]
intervals = ["1m", "5m"]

# Daha önce gönderilen sinyalleri takip etmek için
previous_signals = {}

async def start_signal_loop():
    while True:
        try:
            for symbol in symbols:
                for interval in intervals:
                    key = f"{symbol}_{interval}"
                    try:
                        signal = await analyze_signals(symbol, interval)
                        # Eğer hiç sinyal alınamazsa, gönderme
                        if signal is None:
                            continue

                        # Önceki sinyal ile aynıysa mesaj gönderme
                        if previous_signals.get(key) == signal:
                            continue

                        # Sinyal değişmişse, güncelle ve mesaj gönder
                        previous_signals[key] = signal
                        await send_signal_to_channel(symbol, interval, signal)

                        await asyncio.sleep(3)  # Her bir analiz arasında 3 sn bekle (spam önlemi)

                    except Exception as e:
                        print(f"{symbol} - {interval} analiz hatası: {e}")
                        continue

            await asyncio.sleep(180)  # 3 dakikada bir sinyalleri kontrol et

        except Exception as e:
            print(f"Genel döngü hatası: {e}")
            await asyncio.sleep(180)
