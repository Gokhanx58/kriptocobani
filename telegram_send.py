from telegram import Bot

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "-1002556449131"  # Dikkat: bu ID özel kanal içindir

bot = Bot(token=BOT_TOKEN)

try:
    bot.send_message(chat_id=CHANNEL_ID, text="✅ Test mesajı: Bu mesaj gelirse bağlantı tamam.")
    print("✅ Telegram'a mesaj gönderildi.")
except Exception as e:
    print(f"❌ HATA: {e}")
