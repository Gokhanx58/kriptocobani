# handlers.py

from telegram import Update
from telegram.ext import ContextTypes
from analyzer import analyze_signals

async def handle_analiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args or len(context.args) != 2:
            await update.message.reply_text("Kullanım: /analiz COIN ZAMAN\nÖrnek: /analiz BTCUSDT 5")
            return

        symbol = context.args[0].upper()
        interval = context.args[1]

        result = analyze_signals(symbol, interval, manual=True)
        await update.message.reply_text(result)

    except Exception as e:
        await update.message.reply_text(f"Hata oluştu: {str(e)}")
