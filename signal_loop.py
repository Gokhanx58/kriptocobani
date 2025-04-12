import asyncio
from analyzer import analyze_signals
from telegram_send import send_telegram_message

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]
INTERVALS = ["1m", "5m"]

last_signals = {}

async def start_signal_loop():
    while True:
        for symbol in SYMBOLS:
            for interval in INTERVALS:
                try:
                    key = f"{symbol}_{interval}"
                    result = await analyze_signals(symbol, interval)
                    if result != last_signals.get(key):
                        last_signals[key] = result

                        # Mesajı Telegram formatında hazırla
                        message = f"<b>{symbol} ({interval})</b> için sinyal: <b>{result}</b>"
                        send_telegram_message(message)

                        await asyncio.sleep(3)  # Çakışmayı önlemek için bekleme
                except Exception as e:
                    print(f"Hata ({symbol} - {interval}):", e)
        await asyncio.sleep(180)  # Her 3 dakikada bir kontrol
