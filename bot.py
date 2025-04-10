import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from analysis import analyze_symbol

# Telegram bot tokenınızı buraya ekleyin
TELEGRAM_BOT_TOKEN = '7649989587:AAHUpzkXy3f6ZxoWmNTFUZxXF-XHuJ4DsUw'

# Logging ayarları
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hoş geldiniz! Lütfen analiz yapmak istediğiniz sembolü ve zaman dilimini girin.\nÖrnek: /analyze BTCUSDT 15')

def analyze(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 2:
        update.message.reply_text('Lütfen sembol ve zaman dilimini doğru formatta girin.\nÖrnek: /analyze BTCUSDT 15')
        return
    symbol = context.args[0].upper()
    interval = context.args[1]
    result = analyze_symbol(symbol, interval)
    update.message.reply_text(result)

def start_bot() -> None:
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("analyze", analyze))
    updater.start_polling()
    updater.idle()
