import asyncio
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers import analiz_komutu

nest_asyncio.apply()

app = ApplicationBuilder().token("8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs").build()

# Komut handler'ı tanımlıyoruz
handle_analiz = CommandHandler("analiz", analiz_komutu)
app.add_handler(handle_analiz)

async def main():
    await app.initialize()
    await app.start()
    print("🚀 Bot aktif")
    await app.updater.start_polling()
    await app.updater.idle()

asyncio.run(main())
