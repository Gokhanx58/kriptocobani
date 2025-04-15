# main.py (asyncio ile sinyal döngüsünü başlatır)

import asyncio
from signal_loop import start_signal_loop

if __name__ == "__main__":
    print("🚀 Sinyal botu başlatıldı... İlk analizler gönderilecek.")
    asyncio.run(start_signal_loop())
