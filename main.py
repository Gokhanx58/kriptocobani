import asyncio
from signal_loop import start_signal_loop

if __name__ == "__main__":
    print("🚀 Ana döngü çalışmaya başladı.")  # DEBUG log
    asyncio.run(start_signal_loop())
