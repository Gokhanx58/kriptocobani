from telegram.ext import ApplicationBuilder, MessageHandler, filters
import os

async def handle_message(update, context):
    await update.message.reply_text("Nötr")

application = ApplicationBuilder().token("7649989587:AAHUpzkXy3f6ZxoWmNTFUZxXF-XHuJ4DsUw").build()
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url="https://kriptocobani.onrender.com"
    )
