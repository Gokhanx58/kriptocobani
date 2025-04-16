import asyncio
import logging
from tvdatafeed import TvDatafeed, Interval
from signal_generator import generate_signal
import telegram
from datetime import datetime

# === Telegram Ayarları ===
BOT_TOKEN = '7677308602:AAHH7vloPaQ7PqgFdBnJ2DKYy6sjJ5iqaYE'
CHANNEL_ID = '@GokriptoHan'
bot = telegram.Bot(token=BOT_TOKEN)

# === TradingView Login ===
tv = TvDatafeed(username='marsticaret1', password='8690Yn678690')

# === İzlenecek Semboller ve Zaman Dilimleri ===
SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'SUIUSDT']
INTERVALS = [Interval.MIN_1, Interval.MIN_5]

# === Son gönderilen sinyallerin takibi ===
last_signals = {}

# === Bar sayısı ===
bars = 200

# === Döngü ===
async def run_signal_loop():
    while True:
        for symbol in SYMBOLS:
            for interval in INTERVALS:
                try:
                    df = tv.get_hist(symbol=symbol, interval=interval, n_bars=bars)
                    if df is None or df.empty:
                        continue

                    result = generate_signal(df)
                    if not result:
                        continue

                    last_time, signal = result

                    key = f"{symbol}_{interval.value}"
                    previous = last_signals.get(key)

                    if previous != signal:
                        last_signals[key] = signal

                        message = (
                            f"📊 *Sinyal Geldi!*\n"
                            f"*Sembol:* `{symbol}`\n"
                            f"*Zaman Dilimi:* `{interval.value}`\n"
                            f"*Sinyal:* `{signal}`\n"
                            f"🕒 {last_time.strftime('%Y-%m-%d %H:%M')}"
                        )
                        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")

                except Exception as e:
                    logging.error(f"{symbol} - {interval.value}: HATA → {e}")

        await asyncio.sleep(60)

# === Uygulama başlat ===
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_signal_loop())
