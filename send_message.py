from config import TELEGRAM_TOKEN, TELEGRAM_CHANNEL
from telegram import Bot

bot = Bot(token=TELEGRAM_TOKEN)

def send_telegram_message(message: str):
    print("📤 Telegram'a mesaj gönderiliyor:", message)
    bot.send_message(chat_id=TELEGRAM_CHANNEL, text=message)
