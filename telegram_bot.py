import logging
from telegram import Bot
from config import TELEGRAM_TOKEN, TELEGRAM_CHANNEL

bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram(message: str):
    try:
        await bot.send_message(chat_id=TELEGRAM_CHANNEL, text=message, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Telegram gönderim hatası: {e}")
