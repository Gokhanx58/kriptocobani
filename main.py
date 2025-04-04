import os
from dotenv import load_dotenv

load_dotenv()  # .env dosyasını oku

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from analysis import analyze_pair

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=TOKEN)
app = Flask(__name__)

dispatcher = Dispatcher(bot, None, use_context=True)

def start(update, context):
    update.message.reply_text("Merhaba! Kripto sinyal botuna hoş geldin.")

def handle_message(update, context):
    text = update.message.text.strip()
    if " " in text:
        symbol, interval = text.split()
        response = analyze_pair(symbol.lower(), interval)
        update.message.reply_text(response)
    else:
        update.message.reply_text("Geçerli bir komut girin. Örn: btcusdt 15")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

@app.route('/')
def home():
    return "Bot çalışıyor."

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

if __name__ == "__main__":
    bot.delete_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
