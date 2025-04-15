import asyncio
from analyzer import analyze_signals

async def start_signal_loop():
    print("✅ Sinyal döngüsü başladı.")
    await analyze_signals(initial=True)

    while True:
        try:
            await analyze_signals()
        except Exception as e:
            print(f"⚠️ Döngü hatası: {e}")
        await asyncio.sleep(180)
