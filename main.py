# main.py (geçici test tetiklemesi için)

import asyncio
from signal_loop import start_signal_loop

if __name__ == "__main__":
    print("Sistem başlatıldı. İlk sinyal testi için bekleniyor...")
    asyncio.run(start_signal_loop())
