import httpx
from config import TELEGRAM_TOKEN, TELEGRAM_CHANNEL

async def send_signal_to_channel(symbol, interval, signal_type, signal_price, current_price):
    strength = "GÜÇLÜ " if "GÜÇLÜ" in signal_type else ""
    emoji = "✅" if "AL" in signal_type else "❌"

    message = (
        f"Coin: {symbol}\n"
        f"⏱️ Zaman: {interval}\n"
        f"📊 Sistem: CHoCH + Order Block + FVG\n"
        f"📌 Sinyal: {emoji} {strength}{signal_type.replace('GÜÇLÜ ', '')}\n"
        f"📍 Sinyal Geldiği Fiyat: {signal_price}\n"
        f"💰 Şu Anki Fiyat: {current_price}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHANNEL, "text": message}
    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, data=payload)
    except Exception as e:
        print(f"Telegram gönderim hatası: {e}")
