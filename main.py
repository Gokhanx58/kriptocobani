import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import os

# SABİT TOKEN VE WEBHOOK URL
TOKEN = "7649989587:AAHUpzkXy3f6ZxoWmNTFUZxXF-XHuJ4DsUw"
WEBHOOK_URL = "https://kriptocobani.onrender.com"

# Flask uygulaması
app = Flask(__name__)
bot = Bot(token=TOKEN)

# Dispatcher tanımla
dispatcher = Dispatcher(bot, None, use_context=True)

# Logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# /start komutu
def start(update, context):
    update.message.reply_text("Bot aktif! 👋")

# Genel mesaj yakalayıcı
def echo(update, context):
    text = update.message.text
    update.message.reply_text(f"Mesaj aldım: {text}")

# Handler'lar
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Webhook ayarı
@app.route("/", methods=["GET", "HEAD"])
def index():
    bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    return "Webhook başarıyla ayarlandı."

# Uygulamayı başlat
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
