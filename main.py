import asyncio
from signal_loop import start_signal_loop

if __name__ == "__main__":
    print("Sistem başlatıldı. İlk sinyaller gönderiliyor...")
    asyncio.run(start_signal_loop())
