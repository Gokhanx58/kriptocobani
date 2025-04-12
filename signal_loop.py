# signal_loop.py

import asyncio
from rsi_rmi_analyzer import analyze_signals
from telegram import Bot
import os

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "@GoKriptoLine"

bot = Bot(token=BOT_TOKEN)

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]
intervals = ["1", "5"]
previous_signals = {}

async def start_signal_loop():
    while True:
        try:
            for symbol in symbols:
                for interval in intervals:
                    key = f"{symbol}_{interval}"
                    result = analyze_signals(symbol, interval)

                    if result in ["AL", "SAT", "BEKLE"]:
                        if key not in previous_signals or previous_signals[key] != result:
                            previous_signals[key] = result
                            message = f"{symbol} {interval}dk grafikte sinyal: {result}"
                            await bot.send_message(chat_id=CHANNEL_ID, text=message)
                    
                    await asyncio.sleep(2)  # Her işlem arası bekleme

            await asyncio.sleep(180)  # 3 dakikalık döngü

        except Exception as e:
            print(f"Hata oluştu: {str(e)}")
            await asyncio.sleep(10)
