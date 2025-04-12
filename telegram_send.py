# telegram_send.py

from telegram import Bot

TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "-1002556449131"

async def send_signal_to_channel(message):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHANNEL_ID, text=message)
