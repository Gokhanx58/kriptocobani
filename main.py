# main.py

import asyncio
import nest_asyncio
from signal_loop import start_signal_loop

nest_asyncio.apply()

async def main():
    # Sadece sinyal kontrol döngüsü başlatılır
    asyncio.create_task(start_signal_loop())
    print("Sinyal döngüsü başlatıldı.")
    
    # Sonsuz döngüde sistemin açık kalması sağlanır
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
