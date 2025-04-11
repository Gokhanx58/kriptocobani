import asyncio
from analyzer import analyze_signals

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]
intervals = ["1", "5"]  # sadece 1 dakikalık ve 5 dakikalık grafik

async def check_signals_loop(bot, channel_id):
    while True:
        for symbol in symbols:
            for interval in intervals:
                try:
                    message = analyze_signals(symbol, interval, manual=False)
                    if message and "BEKLE" not in message:
                        await bot.send_message(chat_id=channel_id, text=message)
                    await asyncio.sleep(3)  # Çakışmaları önlemek için gecikme
                except Exception as e:
                    print(f"{symbol}-{interval} analiz hatası:", e)
                    continue
        await asyncio.sleep(30)  # Ana döngü 30 saniyede bir tekrar
