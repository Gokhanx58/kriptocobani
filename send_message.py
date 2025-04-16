from telegram import Bot
from config import TELEGRAM_TOKEN, TELEGRAM_CHANNEL

bot = Bot(token=TELEGRAM_TOKEN)

def format_signal_message(symbol, interval, signal, signal_price, last_close):
    return (
        f"📈 {symbol.upper()} | {interval}\n"
        f"📊 Sistem: CHoCH + Order Block + FVG\n"
        f"📌 Sinyal: {'✅ AL' if 'AL' in signal else '❌ SAT'}\n"
        f"💰 Fiyat: {round(signal_price, 2)} → {round(last_close, 2)}"
    )

async def send_signal_to_channel(symbol, interval, signal, signal_price, last_close):
    try:
        message = format_signal_message(symbol, interval, signal, signal_price, last_close)
        await bot.send_message(chat_id=TELEGRAM_CHANNEL, text=message)
    except Exception as e:
        print(f"📛 Telegram mesaj gönderme hatası: {e}")
