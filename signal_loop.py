import asyncio
from rsi_rmi_analyzer import analyze_signals
from telegram_send import send_signal_to_channel

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]
intervals = ["1", "5"]
previous_signals = {}

async def start_signal_loop():
    while True:
        for symbol in symbols:
            for interval in intervals:
                try:
                    signal = await analyze_signals(symbol, interval)
                    key = f"{symbol}_{interval}"
                    prev = previous_signals.get(key)
                    if signal != prev:
                        previous_signals[key] = signal
                        if signal in ["AL", "SAT", "BEKLE"]:
                            await send_signal_to_channel(symbol, interval, signal)
                    await asyncio.sleep(3)  # Çakışmayı önleme
                except Exception as e:
                    print(f"{symbol} {interval} hata: {e}")
        await asyncio.sleep(180)  # 3 dakika bekle
