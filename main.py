import asyncio
from signal_loop import start_signal_loop

if __name__ == "__main__":
    print("Sistem başlatılıyor...")
    asyncio.run(start_signal_loop())
