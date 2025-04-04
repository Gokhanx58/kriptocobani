import os
import threading
from telegram.ext import CommandHandler, Updater
from flask import Flask

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Telegram bot işlemleri
def start(update, context):
    update.message.reply_text("📈 Kripto Bot aktif! Sinyaller yakında burada olacak.")

def run_telegram_bot():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    updater.start_polling()  # idle kaldırıldı

# Flask sahte sunucu (Render kandırmacası)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot çalışıyor!"

if __name__ == '__main__':
    threading.Thread(target=run_telegram_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
