import os
import requests
from telegram import Bot
from telegram.ext import CommandHandler, Updater
from flask import Flask

app = Flask(__name__)  # bu Render için kandırma kodu

@app.route('/')
def home():
    return "Bot çalışıyor!"

TOKEN = os.getenv("TELEGRAM_TOKEN")

def start(update, context):
    update.message.reply_text("📈 Kripto Bot aktif! Sinyaller yakında burada olacak.")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
