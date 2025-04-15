import asyncio
from signal_loop import start_signal_loop

print("🚀 Bot başlatılıyor...")

async def main():
    await start_signal_loop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"💥 Başlatma hatası: {e}")
