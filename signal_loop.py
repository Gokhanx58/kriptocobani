import asyncio
from analyzer import analyze_signals

async def start_signal_loop():
    while True:
        print("🔁 Yeni analiz başlatıldı...")
        analyze_signals()
        await asyncio.sleep(180)  # 3 dakikada bir sinyal kontrolü
