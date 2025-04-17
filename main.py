import asyncio, logging
from tvdatafeed import TvDatafeed
from config import SYMBOLS, INTERVALS, BARS
from signal_generator import generate_signal
from telegram_bot import send_telegram

async def run_signal_loop():
    logging.basicConfig(level=logging.INFO)
    # TradingView bağlantısı
    tv = TvDatafeed(username="marsticaret1", password="8690Yn678690")
    last_signals = {}

    while True:
        for sym in SYMBOLS:
            for interval in INTERVALS:
                try:
                    df = tv.get_hist(symbol=sym, interval=interval, n_bars=BARS)
                    if df is None or df.empty:
                        logging.warning(f"{sym}-{interval.value}: veri yok")
                        continue

                    signals = generate_signal(df)
                    if not signals:
                        continue

                    ts, sig = signals[-1]
                    key = (sym, interval.value)
                    if last_signals.get(key) != sig:
                        last_signals[key] = sig
                        msg = (
                            f"📊 *Sistem:* CHoCH + Order Block + FVG\n"
                            f"🪙 *Coin:* `{sym}`\n"
                            f"⏱️ *Zaman:* `{interval.value}`\n"
                            f"📌 *Sinyal:* `{sig}`\n"
                            f"🕒 {ts.strftime('%Y-%m-%d %H:%M')}"
                        )
                        await send_telegram(msg)
                except Exception as e:
                    logging.error(f"{sym}-{interval.value}: HATA → {e}")

        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(run_signal_loop())
