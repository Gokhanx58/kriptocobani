import asyncio
from analyzer import analyze_signals

async def start_signal_loop():
    await analyze_signals()
    while True:
        await asyncio.sleep(15)  # spam koruması için kısa gecikme
        await analyze_signals()
