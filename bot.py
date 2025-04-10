from telegram.ext import ApplicationBuilder, MessageHandler, filters
import logging

# Loglama eklendi
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def handle_message(update, context):
    print("Mesaj alındı:", update.message.text)
    await update.message.reply_text("Nötr")

application = ApplicationBuilder().token("7649989587:AAHUpzkXy3f6ZxoWmNTFUZxXF-XHuJ4DsUw").build()
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
