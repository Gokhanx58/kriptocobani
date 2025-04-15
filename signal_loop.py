import asyncio
from analyzer import analyze_signals
from telegram import Bot

BOT_TOKEN = "7677308602:AAHH7vloPaQ7PqgFdBnJ2DKYy6sjJ5iqaYE"
CHANNEL_ID = "@GokriptoHan"
bot = Bot(token=BOT_TOKEN)

symbols = ["BTCUSDT", "ETHUSDT", "AVAXUSDT", "SOLUSDT", "SUIUSDT"]
intervals = [1, 5]  # dakikalık

async def send_message(symbol, interval, signal, entry_price, current_price):
    emoji = "✅" if "AL" in signal else "❌" if "SAT" in signal else "⚠️"
    yorum = {
        "GÜÇLÜ AL": "Yükseliş beklentisi çok güçlü",
        "AL": "Yükseliş bekleniyor",
        "GÜÇLÜ SAT": "Düşüş baskısı yüksek",
        "SAT": "Geri çekilme bekleniyor",
        "BEKLE": "Sinyal oluşumu bekleniyor",
    }.get(signal.replace("KAPAT → ", ""), "Analiz ediliyor...")

    mesaj = (
        f"🪙 Coin: {symbol}\n"
        f"⏱️ Zaman: {interval}m\n"
        f"📊 Sistem: CHoCH + Order Block + FVG\n"
        f"📌 Sinyal: {emoji} {signal} → {yorum}\n"
        f"🎯 Sinyal Fiyatı: {entry_price:.2f}\n"
        f"📉 Güncel Fiyat: {current_price:.2f}"
    )

    try:
        print(f"[Telegram] Gönderiliyor: {signal} - {symbol}-{interval}m")
        await bot.send_message(chat_id=CHANNEL_ID, text=mesaj)
    except Exception as e:
        print(f"[Telegram Hata] {e}")

async def start_signal_loop():
    while True:
        for symbol in symbols:
            for interval in intervals:
                signal, entry, now = analyze_signals(symbol, interval)
                if signal:
                    await send_message(symbol, interval, signal, entry, now)
                await asyncio.sleep(2)  # Coinler arası bekleme
        await asyncio.sleep(180)  # 3 dakikada bir tekrar döngü
