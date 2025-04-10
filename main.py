from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update
import asyncio

TOKEN = "7649989587:AAHUpzkXy3f6ZxoWmNTFUZxXF-XHuJ4DsUw"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Gelen mesaj: {text}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot polling ile çalışıyor...")
    app.run_polling()
