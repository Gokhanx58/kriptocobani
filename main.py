import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import requests
import pandas as pd
import ta

# SABİT TOKEN VE WEBHOOK URL
TOKEN = "7649989587:AAHUpzkXy3f6ZxoWmNTFUZxXF-XHuJ4DsUw"
WEBHOOK_URL = "https://kriptocobani.onrender.com"
API_KEY = "e711a4ec-145e-4215-8420-e3363f2c7a98"  # CoinMarketCap API Anahtarınız

# Flask uygulaması
app = Flask(__name__)
bot = Bot(token=TOKEN)

# Dispatcher tanımla
dispatcher = Dispatcher(bot, None, use_context=True)

# Logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# CoinMarketCap API'den veri çekme fonksiyonu
def fetch_coinmarketcap_data(symbol: str):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        'X-CMC_PRO_API_KEY': API_KEY,
        'Accept': 'application/json',
    }
    params = {
        'symbol': symbol.upper(),
        'convert': 'USD',
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['data']).transpose()
        df['symbol'] = df['symbol'].apply(lambda x: x.upper())
        df['price'] = pd.to_numeric(df['quote']['USD']['price'])
        df['timestamp'] = pd.to_datetime(df['last_updated'])
        return df
    else:
        print(f"CoinMarketCap'den veri alınırken hata oluştu: {response.status_code}")
        return None

# Analiz fonksiyonu (RSI, MACD, EMA analizlerini yapar)
def analyze_pair(symbol: str):
    df = fetch_coinmarketcap_data(symbol)
    if df is None or df.empty:
        return "Veri alınamadı veya geçersiz sembol."

    # RSI
    rsi = ta.momentum.RSIIndicator(close=df["price"], window=14).rsi().iloc[-1]
    # MACD
    macd = ta.trend.MACD(close=df["price"])
    macd_diff = macd.macd_diff().iloc[-1]
    # EMA
    ema_short = ta.trend.EMAIndicator(close=df["price"], window=12).ema_indicator().iloc[-1]
    ema_long = ta.trend.EMAIndicator(close=df["price"], window=26).ema_indicator().iloc[-1]

    # Sinyal üretimi
    sinyaller = []
    if rsi < 30:
        sinyaller.append("RSI: AL")
    elif rsi > 70:
        sinyaller.append("RSI: SAT")
    else:
        sinyaller.append("RSI: BEKLE")

    if macd_diff > 0:
        sinyaller.append("MACD: AL")
    elif macd_diff < 0:
        sinyaller.append("MACD: SAT")
    else:
        sinyaller.append("MACD: BEKLE")

    if ema_short > ema_long:
        sinyaller.append("EMA: AL")
    elif ema_short < ema_long:
        sinyaller.append("EMA: SAT")
    else:
        sinyaller.append("EMA: BEKLE")

    karar = "AL" if sinyaller.count("AL") >= 2 else "SAT" if sinyaller.count("SAT") >= 2 else "BEKLE"

    mesaj = f"{symbol.upper()} analizi\n" + "\n".join(sinyaller) + f"\nSonuç: {karar}"
    return mesaj 

# /start komutu
def start(update, context):
    update.message.reply_text("Bot aktif! 👋")

# Bot komutlarını işlemek için bir fonksiyon ekliyoruz
def handle_commands(update, context):
    command = update.message.text.strip().lower()

    # Desteklenen coinler
    supported_coins = ["btc", "eth", "sui", "avax", "sol"]

    # Komutu kontrol et
    if any(command.startswith(coin) for coin in supported_coins):
        # Komutun iki kısmını ayır
        parts = command.split()
        
        if len(parts) == 2 and parts[1].isdigit():  # Eğer doğru formatta bir komut ise
            symbol = parts[0].lower()
            interval = parts[1]  # Zaman dilimini al
            update.message.reply_text(f"Analiz yapılacak coin: {symbol.upper()}, Zaman dilimi: {interval} dakika.")
            
            # CoinMarketCap API ile veri çekip, analizi yapalım
            analysis_result = analyze_pair(symbol)
            update.message.reply_text(analysis_result)  # Analiz sonucunu gönder

        else:
            update.message.reply_text("Geçerli bir zaman dilimi girin. Örneğin: 'btc 5'.")

# Handler'lar
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_commands))

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Webhook ayarı
@app.route("/set_webhook", methods=["GET", "POST"])
def set_webhook():
    # Webhook'u ayarlıyoruz
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    return "Webhook başarıyla ayarlandı."

# Uygulamayı başlat
@app.route('/')
def home():
    return "Bot aktif ve çalışıyor!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
