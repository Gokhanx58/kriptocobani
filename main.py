import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print(f"Gelen mesaj: {text}")  # Bu log Render’da gözükmeli
    await update.message.reply_text(f"Gelen mesaj: {text}")

app = ApplicationBuilder().token("7649989587:AAHUpzkXy3f6ZxoWmNTFUZxXF-XHuJ4DsUw").build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url="https://kriptocobani.onrender.com"
    )
