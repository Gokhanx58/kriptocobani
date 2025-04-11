# main.py

import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers import handle_analiz
from signal_loop import start_signal_loop

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("analiz", handle_analiz))

    asyncio.create_task(start_signal_loop())  # Sinyal döngüsü paralel başlasın

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
