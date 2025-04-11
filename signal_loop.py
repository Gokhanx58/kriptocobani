import asyncio
import time
from rsi_rmi_analyzer import analyze_signals
from telegram import Bot
from config import TELEGRAM_TOKEN, CHANNEL_ID

bot = Bot(token=TELEGRAM_TOKEN)

# Son gönderilen sinyalleri tutan dict
last_sent_signals = {}

def should_send_signal(symbol, interval, signal):
    key = f"{symbol}_{interval}"
    current_time = time.time()

    if key in last_sent_signals:
        last_signal, last_time = last_sent_signals[key]
        if last_signal == signal and current_time - last_time < 180:  # 3 dakika
            return False

    last_sent_signals[key] = (signal, current_time)
    return True

async def send_telegram_message(message):
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=message)
    except Exception as e:
        print(f"Telegram gönderim hatası: {e}")

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]
intervals = ["1m", "5m"]

async def start_signal_loop():
    while True:
        for symbol in symbols:
            for interval in intervals:
                try:
                    result = await analyze_signals(symbol, interval, manual=False)
                    if result is None:
                        continue
                    signal = result.get("signal")
                    if signal and should_send_signal(symbol, interval, signal):
                        message = f"{symbol} - {interval} sinyali: {signal}"
                        await send_telegram_message(message)
                    await asyncio.sleep(3)  # Her analiz arası gecikme
                except Exception as e:
                    print(f"{symbol} {interval} analiz hatası: {e}")
        await asyncio.sleep(30)  # Döngü arası gecikme
