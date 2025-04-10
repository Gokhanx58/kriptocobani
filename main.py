import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from rsi_rmi_analyzer import analyze_signals, auto_check_signals

# Telegram bot token
TOKEN = "7713417143:AAGBOgQmxKTVetcbc_NGYuz_P6Kn9zTAO5g"

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Komut /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Kripto Çobanı hazır! Örn: btcusdt 5")

# Mesajı işle
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip().upper()
        parts = text.split()

        if len(parts) != 2:
            await update.message.reply_text("⛔ Geçerli format: btcusdt 5")
            return

        symbol = parts[0]
        tf_key = parts[1]

        timeframe_map = {
            "1": "1m", "5": "5m", "15": "15m",
            "30": "30m", "60": "1h", "240": "4h", "1D": "1d"
        }

        if tf_key not in timeframe_map:
            await update.message.reply_text("⛔ Geçersiz zaman dilimi! (1, 5, 15, 30, 60, 240, 1D)")
            return

        timeframe = timeframe_map[tf_key]

        await update.message.reply_text("🔍 Sinyal analizi yapılıyor...")

        result = analyze_signals(symbol, timeframe, manual=True)
        await update.message.reply_text(result)

    except Exception as e:
        logger.error(f"Hata oluştu: {e}")
        await update.message.reply_text("⚠️ Bir hata oluştu.")

# Ana fonksiyon
def main():
    logger.info("Bot başlatılıyor...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Otomatik sinyal kontrol döngüsü
    async def auto_signal_loop():
        while True:
            for symbol in ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]:
                for tf in ["1m", "5m"]:
                    result = analyze_signals(symbol, tf, manual=False)
                    if "🔔" in result:
                        await app.bot.send_message(chat_id=update_chat_id, text=result)
            await asyncio.sleep(60)

    # Chat ID ayarlanmalı: mesaj atan senin kullanıcı ID'n
    global update_chat_id
    update_chat_id = 693383223  # buraya kendi chat_id’n gelecek

    asyncio.get_event_loop().create_task(auto_signal_loop())

    logger.info("Polling başlatılıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
