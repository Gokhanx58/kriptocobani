import asyncio
from analyzer import analyze_signals

async def start_signal_loop():
    # İlk sinyal analizini hemen yap
    await analyze_signals()

    # Sonsuz döngüde sadece sinyal değişimi oldukça tekrar çağrılır
    while True:
        await asyncio.sleep(15)  # Çok düşük gecikme, spam engelleme amaçlı küçük bekleme
        await analyze_signals()
