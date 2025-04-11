# signal_loop.py

import asyncio
from analyzer import analyze_signals
from telegram import Bot

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "-1002556449131"  # Kanal ID

symbol_list = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]
interval_list = ["1", "5"]

async def start_signal_loop():
    bot = Bot(token=BOT_TOKEN)
    while True:
        for symbol in symbol_list:
            for interval in interval_list:
                result = analyze_signals(symbol, interval, manual=False)
                if result != "BEKLE":
                    await bot.send_message(chat_id=CHANNEL_ID, text=f"{symbol} - {interval}m sinyali: {result}")
                await asyncio.sleep(3)
        await asyncio.sleep(30)
