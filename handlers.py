# handlers.py

from telegram import Update
from telegram.ext import ContextTypes
from analyzer import analyze_signals

# /analiz komutu için handler
async def analiz_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) != 2:
            await update.message.reply_text("Kullanım: /analiz <sembol> <zaman_dilimi>\nÖrn: /analiz BTCUSDT 1")
            return
        
        symbol = context.args[0].upper()
        timeframe = context.args[1]

        result = analyze_signals(symbol, timeframe, manual=True)
        await update.message.reply_text(result)

    except Exception as e:
        await update.message.reply_text(f"Hata oluştu: {str(e)}")
