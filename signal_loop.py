import asyncio
from analyzer import analyze_signals
import time

async def start_signal_loop():
    while True:
        analyze_signals()
        await asyncio.sleep(180)
