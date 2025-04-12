# main.py

import asyncio
import nest_asyncio
from signal_loop import start_signal_loop

nest_asyncio.apply()

async def main():
    print("Bot başlatılıyor...")
    await start_signal_loop()

if __name__ == "__main__":
    asyncio.run(main())
