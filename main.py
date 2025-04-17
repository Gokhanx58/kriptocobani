# main.py

import asyncio
import logging
from binance_client import get_klines   # veya TvDatafeed kullanıyorsanız onu import edin
from signal_generator import generate_signal
import telegram

# Telegram ayarları
BOT_TOKEN    = "7677308602:AAHH7vloPaQ7PqgFdBnJ2DKYy6sjJ5iqaYE"
CHANNEL_ID   = "@GokriptoHan"
bot          = telegram.Bot(token=BOT_TOKEN)

# Semboller, zaman dilimleri ve bar sayısı
SYMBOLS   = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'SUIUSDT']
INTERVALS = ['1m', '5m']   # get_klines ile uyumlu string formatta
BARS      = 200

# Son gönderilen sinyalleri tutarız ki tekrar mesaj atmayalım
last_signals = {}

async def run_signal_loop():
    logging.basicConfig(level=logging.INFO)
    while True:
        for symbol in SYMBOLS:
            for interval in INTERVALS:
                try:
                    # 1) Veri çek
                    df = get_klines(symbol, interval, limit=BARS)

                    # 2) Eğer DataFrame boşsa, hatayı logla ve atla
                    if df.empty:
                        logging.warning(f"{symbol}-{interval}: Veri yok veya hata.")
                        continue

                    # 3) Analiz et, sinyal üret
                    signals = generate_signal(df)
                    if not signals:
                        logging.debug(f"{symbol}-{interval}: Sinyal yok.")
                        continue

                    # 4) En son sinyali al, öncekiyle karşılaştır, Telegram’a gönder
                    ts, sig = signals[-1]
                    key = f"{symbol}_{interval}"
                    if last_signals.get(key) != sig:
                        last_signals[key] = sig
                        message = (
                            f"📊 *Sinyal Geldi!*\n"
                            f"*Sembol:* `{symbol}`\n"
                            f"*Zaman Dilimi:* `{interval}`\n"
                            f"*Sinyal:* `{sig}`\n"
                            f"🕒 {ts.strftime('%Y-%m-%d %H:%M')}"
                        )
                        await bot.send_message(
                            chat_id=CHANNEL_ID,
                            text=message,
                            parse_mode="Markdown"
                        )

                except Exception as e:
                    # Her türlü exception’ı burada yakalayıp logluyoruz
                    logging.error(f"{symbol}-{interval}: HATA → {e}")
        # 60 saniye bekle, sonra tekrar et
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(run_signal_loop())
