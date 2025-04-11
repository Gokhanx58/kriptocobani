# main.py

import asyncio
from telegram.ext import ApplicationBuilder
from handlers import handle_analiz

TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(handle_analiz)

if __name__ == '__main__':
    # Render gibi platformlar zaten async loop çalıştırıyor, o yüzden asyncio.run() değil bu yöntem!
    import nest_asyncio
    nest_asyncio.apply()
    app.run_polling()
