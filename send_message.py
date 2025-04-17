import httpx
from config import TELEGRAM_TOKEN, TELEGRAM_CHANNEL

async def send_signal_to_channel(symbol, interval, signal):
    emoji = "✅" if "AL" in signal else "❌"
    msg = f"🪙 Coin: {symbol}\n⏱️ Zaman: {interval.value}\n📌 Sinyal: {emoji} {signal}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        await client.post(url, data={"chat_id": TELEGRAM_CHANNEL, "text": msg})
