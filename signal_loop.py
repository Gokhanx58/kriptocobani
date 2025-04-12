import asyncio
from telegram_send import send_telegram_message

SYMBOLS = ["BTCUSDT"]
INTERVALS = ["1m"]

async def start_signal_loop():
    while True:
        for symbol in SYMBOLS:
            for interval in INTERVALS:
                try:
                    result = "AL"
                    send_telegram_message(f"<b>{symbol} ({interval})</b> için sinyal: <b>{result}</b>")
                    await asyncio.sleep(3)
                except Exception as e:
                    print(f"Hata ({symbol} - {interval}):", e)
        await asyncio.sleep(180)
