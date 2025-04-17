# main.py
import asyncio
import logging
from analyzer import analyze_signals

logging.basicConfig(level=logging.INFO)

async def run():
    while True:
        await analyze_signals()
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(run())
