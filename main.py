from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from analysis import analyze_pair

TOKEN = "7649989587:AAHUpzkXy3f6ZxoWmNTFUZxXF-XHuJ4DsUw"
WEBHOOK_URL = "https://kriptocobani.onrender.com"

app = Flask(__name__)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

def start(update, context):
    update.message.reply_text("Bot aktif! Komut: btcusdt 5")

def handle_command(update, context):
    text = update.message.text.lower().strip()
    parts = text.split()

    if len(parts) == 2 and parts[0] in ["btcusdt", "ethusdt", "solusdt", "avaxusdt", "suiusdt"] and parts[1].isdigit():
        symbol = parts[0]
        interval = parts[1]
        update.message.reply_text(f"Analiz yapılacak coin: {symbol.upper()}, Zaman dilimi: {interval} dakika.")

        try:
            result = analyze_pair(symbol, interval)
            update.message.reply_text(result)
        except Exception as e:
            update.message.reply_text(f"Analiz sırasında hata oluştu: {str(e)}")
    else:
        update.message.reply_text("Komut geçersiz. Örnek: btcusdt 5")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_command))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/set_webhook")
def set_webhook():
    bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    return "Webhook kuruldu."

@app.route("/")
def home():
    return "Bot aktif."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
