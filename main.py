# main.py

import asyncio
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers import analiz_komutu
from signal_loop import start_signal_loop

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"

nest_asyncio.apply()

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("analiz", analiz_komutu))
    asyncio.create_task(start_signal_loop())
    print("Bot çalışıyor...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
