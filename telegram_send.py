# telegram_send.py (güncellenmiş - fiyat bilgisiyle birlikte)

from telegram import Bot

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "@GoKriptoLine"
bot = Bot(token=BOT_TOKEN)

async def send_signal_to_channel(symbol, interval, signal, price):
    emoji = "✅" if signal == "AL" else "❌" if signal == "SAT" else "⏳"
    detay = "Yükseliş bekleniyor" if signal == "AL" else "Geri çekilme bekleniyor" if signal == "SAT" else "Sinyal bekleniyor"
    sistem_durum = "Güçlü AL" if signal == "AL" else "Güçlü SAT" if signal == "SAT" else "Kararsız"

    mesaj = (
        f"🪙 {symbol} | ⏱️ {interval}m\n"
        f"💰 Fiyat: {price:.2f} USDT\n"
        f"📊 Sistem Durumu: {sistem_durum}\n"
        f"📌 Sinyal: {emoji} {signal} → {detay}"
    )

    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=mesaj)
    except Exception as e:
        print(f"Telegram gönderim hatası: {e}")
