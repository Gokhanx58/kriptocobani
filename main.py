import asyncio
import logging
from datetime import datetime
from analyzer import analyze
from tvdatafeed import TvDatafeed, Interval
import telegram

# Log ayarları
logging.basicConfig(level=logging.INFO)

# Telegram ayarları
BOT_TOKEN = '7677308602:AAHH7vloPaQ7PqgFdBnJ2DKYy6sjJ5iqaYE'
CHANNEL_ID = '@GokriptoHan'
bot = telegram.Bot(token=BOT_TOKEN)

# TradingView login
tv = TvDatafeed(username='marsticaret1', password='8690Yn678690')

# Ayarlar
SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'SUIUSDT']
INTERVALS = [Interval.MIN_1, Interval.MIN_5]
N_BARS = 250

last_signals = {}

async def run_signal_loop():
    while True:
        for symbol in SYMBOLS:
            for interval in INTERVALS:
                try:
                    df = tv.get_hist(symbol=symbol, exchange='MEXC', interval=interval, n_bars=N_BARS)

                    if df is None or df.empty:
                        logging.warning(f"{symbol} - {interval.value}: Veri alınamadı veya boş.")
                        continue

                    results = analyze(df)
                    if not results:
                        logging.info(f"{symbol} - {interval.value}: Sinyal üretilmedi.")
                        continue

                    last_time, last_signal = results[-1]
                    key = f"{symbol}_{interval.value}"
                    previous_signal = last_signals.get(key)

                    if previous_signal != last_signal:
                        last_signals[key] = last_signal

                        message = (
                            f"📊 *Sinyal Geldi!*\n"
                            f"*Sembol:* `{symbol}`\n"
                            f"*Zaman Dilimi:* `{interval.value}`\n"
                            f"*Sinyal:* `{last_signal}`\n"
                            f"🕒 {last_time.strftime('%Y-%m-%d %H:%M')}"
                        )

                        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")
                    else:
                        logging.info(f"{symbol} - {interval.value}: Sinyal değişmedi. ({last_signal})")

                except Exception as e:
                    logging.error(f"{symbol} - {interval.value}: HATA → {e}")

        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(run_signal_loop())
