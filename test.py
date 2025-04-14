# test.py (Sadece Telegram mesajı testi için)

import asyncio
from telegram import Bot

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "@GoKriptoLine"
bot = Bot(token=BOT_TOKEN)

async def test():
    mesaj = (
        "📢 *Test Mesajı Başarılı!*\n"
        "Bu mesaj botun çalıştığını gösterir.\n"
        "🪙 Coin: BTCUSDT\n"
        "⏱️ Zaman: 1m\n"
        "📊 Sistem: Güçlü AL\n"
        "📌 Sinyal: ✅ Güçlü AL → Yükseliş beklentisi çok güçlü\n"
        "💰 Fiyat: 84762.00"
    )

    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=mesaj, parse_mode="Markdown")
        print("✅ Telegram mesajı gönderildi.")
    except Exception as e:
        print(f"❌ Telegram gönderim hatası: {e}")

asyncio.run(test())
