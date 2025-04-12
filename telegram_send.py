# telegram_send.py

from telegram import Bot

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "@GoKriptoLine"  # Kanal kullanıcı adı

bot = Bot(token=BOT_TOKEN)

async def send_signal_to_channel(symbol, interval, message):
    interval_text = interval.upper()
    text = f"📊 *{symbol}* - *{interval_text}*\n\n{message}"
    await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode="Markdown")
