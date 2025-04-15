from telegram import Bot
from config import BOT_TOKEN, CHANNEL_ID

bot = Bot(token=BOT_TOKEN)

def send_text(text):
    try:
        bot.send_message(chat_id=CHANNEL_ID, text=text)
    except Exception as e:
        print(f"Mesaj gönderme hatası: {e}")
