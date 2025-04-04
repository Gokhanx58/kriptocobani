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
@app.route("/webhook", methods=["GET", "POST"])
def set_webhook():
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    return "Webhook başarıyla ayarlandı."


# Uygulamayı başlat
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
import logging

# Loglama yapılandırması
logging.basicConfig(level=logging.INFO)

# Botu oluşturduktan sonra loglamayı ekle
logging.info("Bot başarıyla başlatıldı.")

from flask import Flask, request
import os
from telegram import Bot
from telegram.ext import Dispatcher

app = Flask(__name__)

# Bot Token'ınızı ve Webhook URL'nizi environment'dan alın
TOKEN = os.getenv('TOKEN')  # .env dosyasındaki TOKEN değişkenini alır
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # .env dosyasındaki WEBHOOK_URL değişkenini alır

# Telegram botu ve dispatcher'ı oluşturun
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/set_webhook', methods=["GET"])
def set_webhook():
    url = f"{WEBHOOK_URL}/{TOKEN}"
    bot.set_webhook(url=url)
    return "Webhook başarıyla ayarlandı."

@app.route("/webhook", methods=["POST"])
def webhook():
    # Webhook'tan gelen veriyi alın
    data = request.get_json()
    print(data)  # Webhook'dan gelen veriyi görmek için
    # Telegram botunuza gelen mesajları işleyin
    dispatcher.process_update(data)
    return "Webhook received!", 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)
