from telegram import Bot
from config import TELEGRAM_TOKEN, TELEGRAM_CHANNEL

bot = Bot(token=TELEGRAM_TOKEN)

async def send_signal_to_channel(symbol, interval, signal, old_price, current_price):
    emoji = "✅" if "AL" in signal else "❌" if "SAT" in signal else "⏳"
    yorum = {
        "GÜÇLÜ AL": "Yükseliş beklentisi çok güçlü",
        "AL": "Yükseliş bekleniyor",
        "GÜÇLÜ SAT": "Düşüş baskısı yüksek",
        "SAT": "Geri çekilme bekleniyor",
        "BEKLE": "Sinyal oluşumu bekleniyor"
    }.get(signal, "Analiz yapılıyor...")

    mesaj = (
        f"🪙 Coin: {symbol}\n"
        f"⏱️ Zaman: {interval}\n"
        f"📊 Sistem: CHoCH + Order Block + FVG\n"
        f"📌 Sinyal: {emoji} {signal} → {yorum}\n"
        f"📍 Sinyal Geldiği Fiyat: {old_price:.4f}\n"
        f"💰 Şu Anki Fiyat: {current_price:.4f}"
    )

    try:
        await bot.send_message(chat_id=TELEGRAM_CHANNEL, text=mesaj)
    except Exception as e:
        print(f"Telegram gönderim hatası: {e}")
