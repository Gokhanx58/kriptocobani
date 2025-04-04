import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from analysis import analyze_pair

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text("Kripto Çoban'a hoş geldin! Coin sembolü ve zaman dilimini yazarak analiz alabilirsin.\n\n\n\n\n✅Ornek: btcusdt 5")

def handle_message(update, context):
    try:
        text = update.message.text.strip().lower()
        if " " in text:
            symbol, timeframe = text.split(" ")
            result = analyze_pair(symbol, timeframe)
        else:
            symbol = text
            result = analyze_pair(symbol, "5")
        update.message.reply_text(result, parse_mode='HTML')
    except Exception as e:
        logger.error(f"Hata: {e}")
        update.message.reply_text("Bir hata oluştu. Lütfen girdiğiniz sembolü ve zamanı kontrol edin.\n\n⚠️b.tc/usdt 15 gibi boşluklu yazmalısın!")

def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    run_bot()
