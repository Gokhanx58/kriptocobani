import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Nötr")

application = ApplicationBuilder().token("7649989587:AAHUpzkXy3f6ZxoWmNTFUZxXF-XHuJ4DsUw").build()

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    import asyncio

    async def main():
        await application.start()
        await application.updater.start_polling()  # Webhook değil, polling kullanıyoruz
        await application.updater.idle()

    asyncio.run(main())
