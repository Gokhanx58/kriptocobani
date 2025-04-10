import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update
from flask import Flask, request

TOKEN = "7649989587:AAHUpzkXy3f6ZxoWmNTFUZxXF-XHuJ4DsUw"
WEBHOOK_URL = "https://kriptocobani.onrender.com"

app = Flask(__name__)

# Mesaj geldiğinde verilecek cevap
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot çalışıyor!")

# Telegram bot uygulaması
telegram_app = ApplicationBuilder().token(TOKEN).build()
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route("/", methods=["POST"])
def webhook():
    # Gelen Telegram update'ini işle
    telegram_app.update_queue.put_nowait(Update.de_json(request.get_json(force=True), telegram_app.bot))
    return "ok"

# Webhook set işlemi sadece bir kez yapılır
@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    telegram_app.bot.set_webhook(url=WEBHOOK_URL)
    return "Webhook ayarlandı."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
