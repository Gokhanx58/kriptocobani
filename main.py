# main.py

import asyncio
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers import analiz_komutu
from signal_loop import start_signal_loop

# Telegram bot token
BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"

# Event loop çakışmalarını engeller
nest_asyncio.apply()

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # /analiz komutu ekleniyor
    app.add_handler(CommandHandler("analiz", analiz_komutu))

    # Otomatik sinyal döngüsünü başlat
    asyncio.create_task(start_signal_loop(app))

    print("Bot çalışıyor...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
