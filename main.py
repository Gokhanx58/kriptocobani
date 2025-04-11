import asyncio
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers import handle_analiz
from signal_loop import check_signals_loop

TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "-1002556449131"

async def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("analiz", handle_analiz))

    bot = Bot(token=TOKEN)
    
    # Otomatik sinyal döngüsü
    asyncio.create_task(check_signals_loop(bot, CHANNEL_ID))
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
