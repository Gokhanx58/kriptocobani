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
                    final_signal, rsi_result, rmi_result = await analyze_signals(symbol, interval)

                    if final_signal != last_signals.get(key):
                        last_signals[key] = final_signal

                        message = f"<b>{symbol} ({interval})</b>\n"
                        message += f"RSI Swing: <b>{rsi_result}</b>\n"
                        message += f"RMI Trend: <b>{rmi_result}</b>\n"
                        message += f"Sonuç: <b>{final_signal}</b>"

                        await send_telegram_message(message)
                        await asyncio.sleep(3)  # çakışmayı engelle

                except Exception as e:
                    print(f"[signal_loop] Hata ({symbol} - {interval}):", e)

        await asyncio.sleep(180)  # Her 3 dakikada bir tekrar
