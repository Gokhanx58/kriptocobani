# test_send.py

import asyncio
from telegram import Bot

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "@GoKriptoLine"

async def send_test_message():
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text="✅ Bu bir test mesajıdır.")
        print("✅ Mesaj gönderildi.")
    except Exception as e:
        print(f"❌ Telegram gönderim hatası: {e}")

if __name__ == "__main__":
    asyncio.run(send_test_message())
