import asyncio
from datetime import datetime, timedelta
from telegram import Bot
from rsi_rmi_analyzer import analyze_signals

TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "@GoKriptoLine"
bot = Bot(token=TOKEN)

# Gönderilen sinyalleri tutan yapı (3 dakika kontrolü)
sent_signals = {}

async def start_signal_loop():
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]
    intervals = ["1", "5"]

    while True:
        for symbol in symbols:
            for interval in intervals:
                try:
                    result = analyze_signals(symbol, interval)
                    if not result:
                        continue

                    now = datetime.utcnow()
                    key = f"{symbol}_{interval}_{result}"

                    # Eğer aynı sinyal 3 dakika içinde gönderildiyse atla
                    if key in sent_signals and now - sent_signals[key] < timedelta(minutes=3):
                        continue

                    message = f"{symbol} {interval}m sinyali: {result}"
                    await bot.send_message(chat_id=CHANNEL_ID, text=message)

                    sent_signals[key] = now

                except Exception as e:
                    print(f"Hata oluştu: {e}")

                await asyncio.sleep(10)  # Coin arası gecikme

        await asyncio.sleep(30)  # Ana döngü bekleme süresi
