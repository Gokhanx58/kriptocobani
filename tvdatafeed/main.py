import asyncio

if __name__ == "__main__":
    print("🚀 Bot başlatılıyor...")
    try:
        asyncio.run(start_signal_loop())
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
