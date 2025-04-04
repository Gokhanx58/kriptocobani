import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from analysis import analyze_pair  # Coin analiz fonksiyonunu içeriyor

load_dotenv()

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=TOKEN)
app = Flask(__name__)

dispatcher = Dispatcher(bot, None, use_context=True)


# Komut /start yazıldığında çalışan fonksiyon
def start(update, context):
    update.message.reply_text("Merhaba! Coin analizi yapmak için örnek komut: btcusdt 15")


# Mesajları analiz eden ana fonksiyon
def handle_message(update, context):
    try:
        message = update.message.text.lower()
        if " " in message:
            symbol, timeframe = message.split()
            result = analyze_pair(symbol.upper(), timeframe)
            update.message.reply_text(result)
        else:
            update.message.reply_text("Lütfen sembol ve zaman dilimi yazınız. Örnek: btcusdt 15")
    except Exception as e:
        update.message.reply_text(f"Hata: {str(e)}")


# Handler'lar
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))


# Webhook isteğini yakalayan Flask route'u
@app.route(f'/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
        return 'OK'


# Botu başlatan fonksiyon
if __name__ == "__main__":
    bot.delete_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print(f"Webhook kuruldu: {WEBHOOK_URL}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
