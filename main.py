import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from rsi_rmi_analyzer import analyze_signals, auto_check_signals

TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHAT_ID = 1195723889  # Kendi Telegram ID’n

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Komut ile analiz
async def handle_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip().lower()
        parts = text.split()
        if len(parts) != 2:
            await update.message.reply_text("Lütfen sembol ve zaman dilimi girin. Örnek: btcusdt 1")
            return

        symbol = parts[0].upper()
        timeframe = parts[1]
        result = analyze_signals(symbol, timeframe, manual=True)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"Hata oluştu: {e}")

# Otomatik sinyal döngüsü
async def auto_signal_loop(app):
    while True:
        symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]
        timeframes = ["1", "5"]
        for symbol in symbols:
            for tf in timeframes:
                result = analyze_signals(symbol, tf, manual=False)
                if "AL" in result or "SAT" in result:
                    await app.bot.send_message(chat_id=CHAT_ID, text=result)
        await asyncio.sleep(60)

# Bot başlatma
async def main():
    logger.info("Bot başlatılıyor...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", handle_symbol))
    app.add_handler(CommandHandler("help", handle_symbol))
    app.add_handler(CommandHandler("analyze", handle_symbol))
    app.add_handler(CommandHandler(None, handle_symbol))  # Her mesajı yakala
    asyncio.create_task(auto_signal_loop(app))
    logger.info("Polling başlatılıyor...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
