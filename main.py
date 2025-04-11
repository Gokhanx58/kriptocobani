import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from rsi_rmi_analyzer import analyze_signals

TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHAT_ID = "1195723889"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("GoKriptoLine Bot aktif. Sinyal almak için örnek: /analiz BTCUSDT 5")


async def analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        _, symbol, tf = update.message.text.strip().split()
        result = analyze_signals(symbol.upper(), tf, manual=True)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text("Komut hatalı. Doğru kullanım: /analiz BTCUSDT 5")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.message.text.strip().upper()
        if " " in message:
            symbol, tf = message.split()
            result = analyze_signals(symbol, tf, manual=True)
            await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text("Hatalı mesaj. Örnek: btcusdt 5")


async def auto_signal_loop():
    while True:
        for symbol in ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]:
            for tf in ["1", "5"]:
                result = analyze_signals(symbol, tf, manual=False)
                if result != "BEKLE":
                    from telegram import Bot
                    bot = Bot(token=TOKEN)
                    await bot.send_message(chat_id=CHAT_ID, text=f"{symbol} {tf} dakikalık sinyal:\n{result}")
        await asyncio.sleep(60)


async def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("analiz", analyze_command))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    asyncio.create_task(auto_signal_loop())

    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
