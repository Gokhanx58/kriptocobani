from telegram.ext import ApplicationBuilder, MessageHandler, filters

async def handle_message(update, context):
    await update.message.reply_text("Nötr")

application = ApplicationBuilder().token("7649989587:AAHUpzkXy3f6ZxoWmNTFUZxXF-XHuJ4DsUw").build()
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
