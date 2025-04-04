import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from analysis import analyze_pair  # Teknik analiz fonksiyonlarını içeriyor

# Ortam değişkenlerinden token ve webhook adresi alınıyor
TOKEN = os.environ.get("TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = Flask(__name__)
bot = Bot(token=TOKEN)

dispatcher = Dispatcher(bot, None, use_context=True)

# Komut ve mesaj handler’ları
def start(update, context):
    update.message.reply_text("📈 Kripto Çobanı Bot Aktif! Coin sembolü ve zaman gir (örnek: btcusdt 5)")

def handle_message(update, context):
    text = update.message.text.lower()
    try:
        symbol, timeframe = text.split()
        response = analyze_pair(symbol, timeframe)
        update.message.reply_text(response, parse_mode="HTML")
    except Exception as e:
        update.message.reply_text("❗ Lütfen geçerli bir sembol ve zaman dilimi gir (örnek: btcusdt 5)")

# Dispatcher’a handler’ları ekle
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Webhook endpoint’i
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

# Webhook ayarlama
@app.route("/")
def index():
    bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    return "Bot çalışıyor ve webhook ayarlandı!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
