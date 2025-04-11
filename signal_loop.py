import asyncio
from datetime import datetime, timedelta
from telegram import Bot
from rsi_rmi_analyzer import analyze_signals

TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "@GoKriptoLine"
bot = Bot(token=TOKEN)

# Spam kontrolü için gönderilen sinyalleri hatırlama
sent_signals = {}

async def start_signal_loop():
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]
    intervals = ["1", "5"]

    while True:
        for symbol in symbols:
            for interval in intervals:
                try:
                    result = analyze_signals(symbol, interval)
                    message = f"{symbol} {interval}m sinyali: {result}"

                    # Sinyal anahtarı (örnek: "BTCUSDT_1_AL")
                    key = f"{symbol}_{interval}_{result}"
                    now = datetime.utcnow()

                    # 3 dakika içinde aynı sinyal geldiyse atlama
                    if key in sent_signals:
                        last_sent_time = sent_signals[key]
                        if now - last_sent_time < timedelta(minutes=3):
                            continue  # Aynı sinyal 3 dakika içinde tekrar etmesin

                    # Yeni sinyalse mesajı gönder
                    await bot.send_message(chat_id=CHANNEL_ID, text=message)

                    # Gönderilen sinyali kaydet
                    sent_signals[key] = now

                except Exception as e:
                    print(f"Hata oluştu: {e}")

                await asyncio.sleep(3)

        await asyncio.sleep(30)  # Döngü her 30 saniyede bir tekrar eder
