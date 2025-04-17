# main.py
import asyncio
import logging
from tvdatafeed import TvDatafeed, Interval
from signal_generator import generate_signal
import telegram

from config import TELEGRAM_TOKEN, TELEGRAM_CHANNEL, SYMBOLS, INTERVALS, BARS

# Telegram bot
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# TradingView oturumu
tv = TvDatafeed(username='marsticaret1', password='8690Yn678690')

last_signals = {}

async def run_signal_loop():
    logging.basicConfig(level=logging.INFO)
    while True:
        for symbol in SYMBOLS:
            for interval in INTERVALS:
                try:
                    df = tv.get_hist(symbol=symbol, interval=interval, n_bars=BARS)
                    if df is None or df.empty:
                        logging.warning(f"{symbol}-{interval.value}: Veri yok")
                        continue

                    signals = generate_signal(df)
                    if not signals:
                        continue

                    ts, sig = signals[-1]
                    key = f"{symbol}_{interval.value}"
                    if last_signals.get(key) != sig:
                        last_signals[key] = sig
                        mesaj = (
                            f"📊 *Sinyal Geldi!*\n"
                            f"*Sembol:* `{symbol}`\n"
                            f"*Zaman Dilimi:* `{interval.value}`\n"
                            f"*Sinyal:* `{sig}`\n"
                            f"🕒 {ts.strftime('%Y-%m-%d %H:%M')}"
                        )
                        await bot.send_message(chat_id=TELEGRAM_CHANNEL, text=mesaj, parse_mode="Markdown")
                except Exception as e:
                    logging.error(f"{symbol}-{interval.value}: HATA → {e}")
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(run_signal_loop())
