import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from rsi_rmi_analyzer import analyze_signals
import asyncio
import os

TOKEN = os.getenv("TOKEN", "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Sinyal almak için örnek: /analiz BTCUSDT 5")

async def analiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper()
        interval = context.args[1]
        chat_id = update.effective_chat.id
        result = analyze_signals(symbol, interval, manual=True, chat_id=chat_id)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"Hata: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analiz", analiz))
    app.run_polling()

if __name__ == "__main__":
    main()
