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

# Bot komutlarını işlemek için bir fonksiyon ekliyoruz
def handle_commands(update, context):
    command = update.message.text.strip().lower()

    # 'btcusdt' komutunu kontrol et
    if command.startswith("btcusdt"):
        # Komutun iki kısmını ayır
        parts = command.split()
        
        if len(parts) == 2 and parts[1].isdigit():  # Eğer doğru formatta bir komut ise
            interval = parts[1]  # Zaman dilimini al
            update.message.reply_text(f"Analiz yapılacak coin: BTC/USDT, Zaman dilimi: {interval} dakika.")
        else:
            update.message.reply_text("Geçerli bir zaman dilimi girin. Örneğin: 'Btcusdt 5'.")

# Handler'lar
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_commands))

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Webhook ayarı
@app.route("/set_webhook", methods=["GET", "POST"])
def set_webhook():
    # Webhook'u ayarlıyoruz
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    return "Webhook başarıyla ayarlandı."

# Uygulamayı başlat
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
