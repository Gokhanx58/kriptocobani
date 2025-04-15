import asyncio
from telegram import Bot

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "-1002556449131"  # ID doğru

bot = Bot(token=BOT_TOKEN)

async def test_send():
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text="✅ Bu bir test mesajıdır (await ile).")
        print("✅ Telegram'a mesaj başarıyla gönderildi.")
    except Exception as e:
        print(f"❌ HATA: {e}")

asyncio.run(test_send())
