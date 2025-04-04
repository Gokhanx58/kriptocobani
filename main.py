import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
from analysis import analyze_pair
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text("Merhaba! Teknik analiz için örnek komut: btcusdt 15")


def help_command(update, context):
    update.message.reply_text("Komut formatı: <sembol> <zaman>. Örn: btcusdt 15")


def handle_message(update, context):
    text = update.message.text.strip()
    parts = text.lower().split()

    if len(parts) != 2:
        update.message.reply_text("Geçersiz komut. Örn: btcusdt 15")
        return

    symbol, interval = parts

    try:
        result = analyze_pair(symbol.upper(), interval)
        update.message.reply_text(result, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(f"Hata oluştu: {e}")
        update.message.reply_text("Analiz sırasında hata oluştu. Lütfen tekrar deneyin.")


def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run_bot()
