from telegram import Bot
import asyncio

BOT_TOKEN = "7677308602:AAHH7vloPaQ7PqgFdBnJ2DKYy6sjJ5iqaYE"
CHANNEL_ID = "@GokriptoHan"
bot = Bot(token=BOT_TOKEN)

async def send_signal(symbol, interval, signal, entry_price, current_price):
    emoji = "✅" if "AL" in signal else "❌" if "SAT" in signal else "⏳"
    yorum = {
        "GÜÇLÜ AL": "Yükseliş beklentisi çok güçlü",
        "AL": "Yükseliş bekleniyor",
        "GÜÇLÜ SAT": "Düşüş baskısı yüksek",
        "SAT": "Geri çekilme bekleniyor",
        "BEKLE": "Sinyal oluşumu bekleniyor"
    }.get(signal.upper(), "Analiz yapılıyor...")

    mesaj = (
        f"🪙 Coin: {symbol}\n"
        f"⏱️ Zaman: {interval}m\n"
        f"📊 Sistem: CHoCH + Order Block + FVG\n"
        f"📌 Sinyal: {emoji} {signal.upper()} → {yorum}\n"
        f"🎯 Sinyal Geldiği Fiyat: {entry_price:.4f}\n"
        f"💰 Şu Anki Fiyat: {current_price:.4f}"
    )

    try:
        print(f"[Telegram] Gönderiliyor: {mesaj}")
        await bot.send_message(chat_id=CHANNEL_ID, text=mesaj)
    except Exception as e:
        print(f"[Telegram] Hata oluştu: {e}")
