import asyncio
from signal_loop import start_signal_loop

if __name__ == "__main__":
    print("\U0001F680 Bot başlatılıyor...")
    asyncio.run(start_signal_loop())
