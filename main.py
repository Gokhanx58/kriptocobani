import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from rsi_rmi_analyzer import analyze_signals, auto_check_signals

# Telegram bot token ve chat_id
TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHAT_ID = 1195723889  # Senin kullanıcı ID'in

# Aktif coinler ve zaman dilimleri
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]
INTERVALS = ["1", "5"]  # Sadece 1m ve 5m için otomatik sinyal
DELAY = 60  # saniye cinsinden (60 saniyede bir kontrol)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Komut ile analiz yapma fonksiyonu
async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if not args:
            await update.message.reply_text("Kullanım: /analiz BTCUSDT 1")
            return

        symbol = args[0].upper()
        interval = args[1] if len(args) > 1 else "1"
        result = analyze_signals(symbol, interval, manual=True)
        await update.message.reply_text(result)

    except Exception as e:
        await update.message.reply_text(f"Hata: {str(e)}")

# Botu başlatan fonksiyon
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("analiz", handle_command))
    await app.initialize()
    await app.start()
    await app.bot.send_message(chat_id=CHAT_ID, text="🚀 Bot başlatıldı!")
    await auto_check_signals(app.bot, CHAT_ID, SYMBOLS, INTERVALS, DELAY)
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
