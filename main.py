import os
import logging
from flask import Flask, request
from telegram import Bot, ParseMode, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from analysis import analyze_pair
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TOKEN)

# Webhook URL Render ortamında otomatik atanır
APP_URL = os.getenv("RENDER_EXTERNAL_URL") or "https://your-render-url.onrender.com"

app = Flask(__name__)

# Log ayarları
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Dispatcher tanımı
dp = Dispatcher(bot, None, use_context=True)

# Komut işleyici
def handle_message(update: Update, context):
    try:
        text = update.message.text.strip().lower()
        parts = text.split()

        if len(parts) != 2:
            update.message.reply_text("Komut formatı yanlış. Örnek: btcusdt 15")
            return

        symbol, interval = parts
        reply = analyze_pair(symbol.upper(), interval)
        update.message.reply_text(reply, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    except Exception as e:
        update.message.reply_text(f"Hata oluştu: {str(e)}")

# /start komutu
def start(update: Update, context):
    update.message.reply_text("Merhaba! Coin analiz botuna hoş geldin. Örnek kullanım: btcusdt 15")

# Komutları dispatcher'a bağla
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)
    return "OK"

# Başlangıç
@app.route("/")
def index():
    return "Bot çalışıyor."

def set_webhook():
    webhook_url = f"{APP_URL}/{TOKEN}"
    success = bot.set_webhook(url=webhook_url)
    if success:
        print(f"Webhook ayarlandı: {webhook_url}")
    else:
        print("Webhook ayarlanamadı!")

if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
