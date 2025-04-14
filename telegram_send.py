# telegram_send.py (gelişmiş mesaj yapısıyla)

from telegram import Bot

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "@GoKriptoLine"
bot = Bot(token=BOT_TOKEN)

async def send_signal_to_channel(symbol, interval, signal):
    emoji = "✅" if signal == "AL" else "❌" if signal == "SAT" else "⏳"
    detay = "Yükseliş bekleniyor" if signal == "AL" else "Geri çekilme bekleniyor" if signal == "SAT" else "Sinyal bekleniyor"

    mesaj = (
        f"🪙 Coin: {symbol}\n"
        f"⏱️ Zaman: {interval}m\n"
        f"📊 Sistem: CHoCH + Order Block + FVG\n"
        f"🔍 Yön: {signal}\n"
        f"📌 Sinyal: {emoji} {signal} → {detay}"
    )

    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=mesaj)
    except Exception as e:
        print(f"Telegram gönderim hatası: {e}")
