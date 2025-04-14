# telegram_send.py (renkli, sade, fiyatlı + ilk mesaj tetikleyici)

from telegram import Bot

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "@GoKriptoLine"
bot = Bot(token=BOT_TOKEN)

# İlk gönderim tetikleyicisi
first_sent = set()

async def send_signal_to_channel(symbol, interval, signal, price):
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
        f"⏱️ Zaman: {interval}m\n"
        f"📊 Sistem: {signal}\n"
        f"📌 Sinyal: {emoji} {signal} → {yorum}\n"
        f"💰 Fiyat: {price:.4f}"
    )

    key = f"{symbol}_{interval}"
    if key not in first_sent:
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=mesaj)
            first_sent.add(key)
        except Exception as e:
            print(f"Telegram gönderim hatası: {e}")
