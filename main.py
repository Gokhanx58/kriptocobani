# main.py

import asyncio
from signal_loop import start_signal_loop

async def main():
    print("Sinyal kontrol sistemi başlatılıyor...")
    while True:
        await start_signal_loop()
        await asyncio.sleep(180)  # 3 dakika bekle

if __name__ == "__main__":
    asyncio.run(main())
