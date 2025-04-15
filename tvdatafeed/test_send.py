import asyncio
from telegram import Bot

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "@GoKriptoLine"

async def test():
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHANNEL_ID, text="✅ Bu bir test mesajıdır.")

if __name__ == "__main__":
    print("🟡 Telegram test başlatılıyor...")
    asyncio.run(test())
