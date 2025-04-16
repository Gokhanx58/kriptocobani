import httpx
from config import TELEGRAM_TOKEN, TELEGRAM_CHANNEL

async def send_signal_to_channel(symbol, interval, signal_type):
    emoji = "✅" if "AL" in signal_type else "❌" if "SAT" in signal_type else "⏳"

    message = (
        f"🪙 Coin: {symbol}\n"
        f"⏱️ Zaman: {interval}\n"
        f"📊 Sistem: CHoCH + Order Block + FVG\n"
        f"📌 Sinyal: {emoji} {signal_type}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHANNEL, "text": message}

    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, data=payload)
    except Exception as e:
        print(f"Telegram gönderim hatası: {e}")
