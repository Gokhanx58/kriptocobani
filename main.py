import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from rsi_rmi_analyzer import analyze_signals, auto_signal_runner

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Komutlar hazır. Örnek: /analiz BTCUSDT 5")

async def analiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pair = context.args[0].upper()
        interval = context.args[1]
        result = analyze_signals(pair, interval, manual=True)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"Hata: {str(e)}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("analiz", analiz))

async def main():
    asyncio.create_task(auto_signal_runner(app.bot, "BTCUSDT", ["1"]))
    await asyncio.sleep(3)
    asyncio.create_task(auto_signal_runner(app.bot, "BTCUSDT", ["5"]))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
