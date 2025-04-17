import asyncio
import logging
import telegram
from tvdatafeed import TvDatafeed
from config import TELEGRAM_TOKEN, TELEGRAM_CHANNEL, SYMBOLS, INTERVALS, BARS
from signal_generator import generate_signal

# Logging yapılandırması
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

# Telegram bot
bot = telegram.Bot(token=TELEGRAM_TOKEN)
# TradingView bağlantısı
tv = TvDatafeed(username='marsticaret1', password='8690Yn678690')

# Önceki sinyaller takibi\last_signals = {}

async def run_signal_loop():
    while True:
        for symbol in SYMBOLS:
            for interval in INTERVALS:
                try:
                    df = tv.get_hist(symbol=symbol, interval=interval, n_bars=BARS)
                    logging.debug(f"{symbol}-{interval.value}: df uzunluğu = {len(df)}, index dtype = {df.index.dtype}")
                    if df is None or df.empty:
                        logging.warning(f"{symbol}-{interval.value}: Veri yok")
                        continue

                    signals = generate_signal(df)
                    logging.debug(f"{symbol}-{interval.value}: Sinyaller = {signals}")
                    if not signals:
                        continue

                    ts, sig = signals[-1]
                    key = f"{symbol}_{interval.value}"
                    if last_signals.get(key) != sig:
                        last_signals[key] = sig
                        message = (
                            f"📊 *Sinyal Geldi!*\n"
                            f"*Sembol:* `{symbol}`\n"
                            f"*Zaman Dilimi:* `{interval.value}`\n"
                            f"*Sinyal:* `{sig}`\n"
                            f"🕒 {ts.strftime('%Y-%m-%d %H:%M')}"
                        )
                        await bot.send_message(chat_id=TELEGRAM_CHANNEL, text=message, parse_mode="Markdown")
                        logging.info(f"Gönderilen sinyal: {symbol} {interval.value} → {sig} @ {ts}")
                except Exception as e:
                    logging.error(f"{symbol}-{interval.value}: HATA → {e}")
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(run_signal_loop())
