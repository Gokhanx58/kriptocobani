import asyncio
from analyzer import analyze_signals

symbols = ["BTCUSDT", "ETHUSDT", "AVAXUSDT", "SOLUSDT", "SUIUSDT"]
timeframes = [1, 5]  # dakika

async def start_signal_loop():
    print("✅ Sinyal döngüsü başladı.")
    while True:
        for symbol in symbols:
            for tf in timeframes:
                try:
                    print(f"🔍 Analiz ediliyor: {symbol}-{tf}m")
                    await analyze_signals(symbol, tf)
                    await asyncio.sleep(3)
                except Exception as e:
                    print(f"❌ {symbol} {tf} analiz hatası: {e}")
        await asyncio.sleep(180)
