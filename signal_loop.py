import asyncio
from analyzer import analyze_signals

async def start_signal_loop():
    while True:
        await analyze_signals()
        await asyncio.sleep(180)
