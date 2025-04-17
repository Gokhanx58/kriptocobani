import asyncio
import logging
from config import TELEGRAM_TOKEN, TELEGRAM_CHANNEL, SYMBOLS, INTERVALS, BARS
from signal_generator import generate_signals
from tvdatafeed import TvDatafeed
import telegram

logging.basicConfig(level=logging.DEBUG)
bot = telegram.Bot(token=TELEGRAM_TOKEN)
tv  = TvDatafeed(username="marsticaret1", password="8690Yn678690")
last_signals = {}

async def run_loop():
    while True:
        for sym in SYMBOLS:
            for interval in INTERVALS:
                try:
                    df = tv.get_hist(sym, interval, n_bars=BARS)
                    if df.empty:
                        logging.warning(f"{sym}-{interval}: veri yok")
                        continue

                    signals = generate_signals(df)
                    if not signals:
                        logging.debug(f"{sym}-{interval}: CHoCH yok, sinyal üretilmedi.")
                        continue

                    ts, sig = signals[-1]
                    key = f"{sym}_{interval.value}"
                    if last_signals.get(key) != sig:
                        last_signals[key] = sig
                        msg = (
                            f"📊 *Sinyal Geldi!*\n"
                            f"*Sembol:* `{sym}`\n"
                            f"*Zaman Dilimi:* `{interval.value}`\n"
                            f"*Sinyal:* `{sig}`\n"
                            f"🕒 {ts.strftime('%Y-%m-%d %H:%M')}"
                        )
                        await bot.send_message(chat_id=TELEGRAM_CHANNEL,
                                               text=msg, parse_mode="Markdown")
                except Exception as e:
                    logging.error(f"{sym}-{interval}: HATA → {e}")
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(run_loop())
