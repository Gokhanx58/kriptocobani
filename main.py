from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram import Update
import asyncio

async def handle_message(update: Update, context):
    await update.message.reply_text("Bot aktif, mesajını aldım!")

async def main():
    app = ApplicationBuilder().token("7649989587:AAHUpzkXy3f6ZxoWmNTFUZxXF-XHuJ4DsUw").build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
