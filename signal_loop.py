# signal_loop.py

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
                    final_signal, rsi_swing_signal, rmi_signal = await analyze_signals(symbol, interval)

                    if last_signals.get(key) != final_signal:
                        last_signals[key] = final_signal
                        send_telegram_message(symbol, interval, final_signal, rsi_swing_signal, rmi_signal)
                        await asyncio.sleep(3)  # Çakışmayı önlemek için gecikme

                except Exception as e:
                    print(f"HATA: {symbol} - {interval}: {e}")

        await asyncio.sleep(180)  # 3 dakikada bir kontrol
