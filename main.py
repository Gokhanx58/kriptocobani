import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from rsi_rmi_analyzer import analyze_signals, auto_check_signals

TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHAT_ID = 1195723889  # Kendi kullanıcı ID'in

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot çalışıyor!")

async def analiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) != 2:
            await update.message.reply_text("Komut formatı: /analiz COIN ZAMAN")
            return
        symbol = context.args[0].upper()
        timeframe = context.args[1]
        result = analyze_signals(symbol, timeframe, manual=True)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"Hata oluştu: {e}")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analiz", analiz))

    loop = asyncio.get_running_loop()
    loop.create_task(auto_check_signals(app.bot, CHAT_ID))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
