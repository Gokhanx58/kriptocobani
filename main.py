import asyncio
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers import analiz_komutu

nest_asyncio.apply()

TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"

app = ApplicationBuilder().token(TOKEN).build()

# Komut handler'ı tanımlıyoruz
handle_analiz = CommandHandler("analiz", analiz_komutu)
app.add_handler(handle_analiz)

async def main():
    await app.initialize()
    await app.start()
    print("Bot başlatıldı")
    await app.updater.start_polling()
    await app.updater.idle()

asyncio.run(main())
