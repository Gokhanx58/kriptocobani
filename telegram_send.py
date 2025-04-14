from telegram import Bot

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "@GoKriptoLine"
bot = Bot(token=BOT_TOKEN)

async def send_signal_to_channel(symbol, interval, signal):
    mesaj = f"{symbol} | {interval} dk → Sinyal: {signal}"
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=mesaj)
    except Exception as e:
        print(f"Telegram gönderim hatası: {e}")
