import pandas as pd
from datetime import datetime
from tvdatafeed import TvDatafeed, Interval
from telegram import Bot
from utils import round_to_nearest

tv = TvDatafeed(username="marsticaret1", password="8690Yn678690")
bot = Bot(token="7677308602:AAHH7vloPaQ7PqgFdBnJ2DKYy6sjJ5iqaYE")
CHANNEL_ID = "@GokriptoHan"

last_sent = {}

symbols = ["BTCUSDT", "ETHUSDT", "AVAXUSDT", "SOLUSDT", "SUIUSDT"]
intervals = {
    "1m": Interval.in_1_minute,
    "5m": Interval.in_5_minute
}

def detect_signal(df):
    latest_close = df["close"].iloc[-1]
    previous_close = df["close"].iloc[-2]
    signal_price = df["close"].iloc[-3]

    if latest_close > previous_close and previous_close > df["close"].iloc[-3]:
        return "AL", signal_price
    elif latest_close < previous_close and previous_close < df["close"].iloc[-3]:
        return "SAT", signal_price
    return "BEKLE", None

async def analyze_signals(initial=False):
    for symbol in symbols:
        for int_name, int_enum in intervals.items():
            try:
                print(f"🔍 Analiz ediliyor: {symbol}-{int_name}")
                df = tv.get_hist(symbol=symbol, exchange="MEXC", interval=int_enum, n_bars=200)
                if df is None or df.empty:
                    print(f"⛔ Veri alınamadı: {symbol}-{int_name}")
                    continue

                sinyal, sinyal_fiyati = detect_signal(df)
                anlik_fiyat = df["close"].iloc[-1]
                key = f"{symbol}_{int_name}"

                if initial or key not in last_sent:
                    last_sent[key] = sinyal
                    await send_signal(symbol, int_name, sinyal, sinyal_fiyati, anlik_fiyat)
                elif sinyal != last_sent[key]:
                    await send_signal(symbol, int_name, sinyal, sinyal_fiyati, anlik_fiyat)
                    last_sent[key] = sinyal
            except Exception as e:
                print(f"❌ {symbol} {int_name} analiz hatası: {e}")

async def send_signal(symbol, interval, signal, signal_price, current_price):
    emoji = "✅" if "AL" in signal else "❌" if "SAT" in signal else "⏳"
    yorum = {
        "Güçlü AL": "Yükseliş beklentisi çok güçlü",
        "AL": "Yükseliş bekleniyor",
        "Güçlü SAT": "Düşüş baskısı yüksek",
        "SAT": "Geri çekilme bekleniyor",
        "BEKLE": "Sinyal oluşumu bekleniyor"
    }.get(signal, "Analiz yapılıyor...")

    mesaj = (
        f"🪙 Coin: {symbol}\n"
        f"⏱️ Zaman: {interval}\n"
        f"📊 Sistem: CHoCH + Order Block + FVG\n"
        f"📌 Sinyal: {emoji} {signal} → {yorum}\n"
        f"💹 Sinyal Geldiği Fiyat: {round_to_nearest(signal_price)}\n"
        f"💰 Şu Anki Fiyat: {round_to_nearest(current_price)}"
    )
    try:
        print(f"📬 Telegram mesajı gönderiliyor: {mesaj}")
        await bot.send_message(chat_id=CHANNEL_ID, text=mesaj)
    except Exception as e:
        print(f"📛 Telegram gönderim hatası: {e}")
