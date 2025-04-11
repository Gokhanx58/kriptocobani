# signal_loop.py

import asyncio
from rsi_rmi_analyzer import analyze_signals
from telegram import Bot
from config import CHANNEL_ID, TELEGRAM_TOKEN

coin_pairs = ["BTCUSDT", "ETHUSDT", "AVAXUSDT", "SOLUSDT", "SUIUSDT"]
timeframes = ["1m", "5m"]

bot = Bot(token=TELEGRAM_TOKEN)

# Son gönderilen sinyalleri tutan bellek
last_signals = {}

async def start_signal_loop():
    while True:
        for symbol in coin_pairs:
            for interval in timeframes:
                try:
                    result = await analyze_signals(symbol, interval, manual=False)
                    key = f"{symbol}_{interval}"
                    if result and result != last_signals.get(key):
                        last_signals[key] = result
                        await bot.send_message(chat_id=CHANNEL_ID, text=f"{symbol} - {interval} sinyali: {result}")
                    await asyncio.sleep(3)  # Her sembol arası gecikme
                except Exception as e:
                    print(f"Hata oluştu: {e}")
        await asyncio.sleep(180)  # Tüm döngü 3 dakikada bir tekrar eder
