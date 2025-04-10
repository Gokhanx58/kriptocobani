from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from analysis import analyze_symbol

TOKEN = "7649989587:AAHUpzkXy3f6ZxoWmNTFUZxXF-XHuJ4DsUw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hoş geldin! Sembol ve zaman dilimi girerek analiz alabilirsin.\nÖrnek: btcusdt 15")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.lower()
        parts = text.split()
        if len(parts) == 2:
            symbol, timeframe = parts
            result = analyze_symbol(symbol.upper(), timeframe)
            await update.message.reply_text(result)
        else:
            await update.message.reply_text("Hatalı komut. Örnek: btcusdt 15")
    except Exception as e:
        await update.message.reply_text(f"Hata oluştu: {str(e)}")

def start_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
