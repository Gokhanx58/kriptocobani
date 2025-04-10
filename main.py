import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from analysis import analyze_rmi_rsi

# Telegram bot token
TOKEN = "7649989587:AAHUpzkXy3f6ZxoWmNTFUZxXF-XHuJ4DsUw"

# Desteklenen semboller ve borsa isimleri
supported_symbols = {
    "BTCUSDT": "BINANCE",
    "ETHUSDT": "BINANCE",
    "SOLUSDT": "BINANCE",
    "AVAXUSDT": "BINANCE",
    "SUIUSDT": "MEXC"
}

# Desteklenen zaman dilimleri
timeframes = {
    "1": "1m",
    "5": "5m",
    "15": "15m",
    "30": "30m",
    "60": "1h",
    "240": "4h",
    "1d": "1d"
}

# Başlangıç komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Kripto Çobanı hazır! Örn: btcusdt 5")

# Kullanıcıdan gelen mesajları işleme
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip().upper()
        parts = text.split()

        if len(parts) != 2:
            await update.message.reply_text("⛔ Geçerli format: btcusdt 5")
            return

        symbol = parts[0]
        tf_key = parts[1]

        if symbol not in supported_symbols:
            await update.message.reply_text(f"⛔ Desteklenmeyen sembol: {symbol}")
            return

        if tf_key not in timeframes:
            await update.message.reply_text("⛔ Zaman dilimi yanlış! (1, 5, 15, 30, 60, 240, 1d)")
            return

        timeframe = timeframes[tf_key]
        exchange = supported_symbols[symbol]

        await update.message.reply_text("📊 Analiz yapılıyor...")

        result = analyze_rmi_rsi(symbol=symbol, exchange=exchange, timeframe=timeframe)
        await update.message.reply_text(f"📈 {symbol} ({timeframe}): {result}")

    except Exception as e:
        logging.error(f"Hata: {e}")
        await update.message.reply_text("⚠️ Beklenmeyen bir hata oluştu.")

# Main bot çalıştırma fonksiyonu
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot polling ile çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
