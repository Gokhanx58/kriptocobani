from telegram.ext import ApplicationBuilder, CommandHandler

async def start(update, context):
    await update.message.reply_text("Bot çalışıyor!")

def start_bot():
    import asyncio
    from telegram.ext import ApplicationBuilder

    application = ApplicationBuilder().token("7649989587:AAHUpzkXy3f6ZxoWmNTFUZxXF-XHuJ4DsUw").build()
    application.add_handler(CommandHandler("start", start))
    asyncio.run(application.run_polling())
