import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import os
import requests
import pandas as pd
import ta

# SABİT TOKEN VE WEBHOOK URL
TOKEN = "7649989587:AAHUpzkXy3f6ZxoWmNTFUZxXF-XHuJ4DsUw"
WEBHOOK_URL = "https://kriptocobani.onrender.com"

# Flask uygulaması
app = Flask(__name__)
bot = Bot(token=TOKEN)

# Dispatcher tanımla
dispatcher = Dispatcher(bot, None, use_context=True)

# Logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# CoinGecko API'den veri çekme fonksiyonu
def fetch_ohlcv(symbol: str, interval: str, limit: int = 100):
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/ohlc?vs_currency=usd&days=1&interval={interval}"
    
    try:
        response = requests.get(url)  # API'ye istek atıyoruz
        response.raise_for_status()  # Eğer hata varsa burada raise edecek
        print(f"API Yanıtı: {response.json()}")  # API'den gelen yanıtı görmek için yazdırıyoruz
        data = response.json()  # JSON veriyi alıyoruz
        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])  # Veriyi pandas DataFrame'e çeviriyoruz
        df["close"] = pd.to_numeric(df["close"])  # 'close' sütununu sayıya dönüştürüyoruz
        print(f"Veri Çekildi: {df.head()}")  # Çekilen veriyi kontrol etmek için ilk 5 satırı yazdırıyoruz
        return df
    except requests.exceptions.HTTPError as err:  # HTTP hatası olursa
        print(f"HTTP Hatası: {err}")
    except Exception as e:  # Diğer hatalar için
        print(f"Veri Çekme Hatası: {e}")
    return None  # Eğer bir hata oluşursa None dönecek

# Analiz fonksiyonu (RSI, MACD, EMA analizlerini yapar)
def analyze_pair(symbol: str, interval: str):
    df = fetch_ohlcv(symbol, interval)
    if df is None or df.empty:
        return "Veri alınamadı veya geçersiz sembol/zaman dilimi."

    # RSI
    rsi = ta.momentum.RSIIndicator(close=df["close"], window=14).rsi().iloc[-1]
    # MACD
    macd = ta.trend.MACD(close=df["close"])
    macd_diff = macd.macd_diff().iloc[-1]
    # EMA
    ema_short = ta.trend.EMAIndicator(close=df["close"], window=12).ema_indicator().iloc[-1]
    ema_long = ta.trend.EMAIndicator(close=df["close"], window=26).ema_indicator().iloc[-1]

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

    mesaj = f"{symbol.upper()} / {interval} analizi\n" + "\n".join(sinyaller) + f"\nSonuç: {karar}"
    print(f"Analiz Sonucu: {mesaj}")  # Analiz sonucunu görmek için print ekledik
    return mesaj 

# /start komutu
def start(update, context):
    update.message.reply_text("Bot aktif! 👋")

# Bot komutlarını işlemek için bir fonksiyon ekliyoruz
def handle_commands(update, context):
    command = update.message.text.strip().lower()

    # 'btcusdt' komutunu kontrol et
    if command.startswith("btcusdt"):
        # Komutun iki kısmını ayır
        parts = command.split()
        
        if len(parts) == 2 and parts[1].isdigit():  # Eğer doğru formatta bir komut ise
            interval = parts[1]  # Zaman dilimini al
            update.message.reply_text(f"Analiz yapılacak coin: BTC/USDT, Zaman dilimi: {interval} dakika.")
            
            # CoinGecko API ile veri çekip, analizi yapalım
            analysis_result = analyze_pair("btcusdt", interval)
            update.message.reply_text(analysis_result)  # Analiz sonucunu gönder

        else:
            update.message.reply_text("Geçerli bir zaman dilimi girin. Örneğin: 'Btcusdt 5'.")

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
