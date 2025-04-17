import asyncio
import logging
from tvdatafeed import TvDatafeed, Interval
from signal_generator import generate_signal
import telegram

BOT_TOKEN   = "7677308602:AAHH7vloPaQ7PqgFdBnJ2DKYy6sjJ5iqaYE"
CHANNEL_ID  = "@GokriptoHan"
bot         = telegram.Bot(token=BOT_TOKEN)

tv = TvDatafeed(
    username="marsticaret1",
    password="8690Yn678690",
    session_signature="v3:iz6molF7z3oCKrettxY7v1u1cSvcjCnPflkvM0Pst3E="
)

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]
INTERVALS = [Interval.MIN_1, Interval.MIN_5]
BARS = 200

last_signals = {}

async def run_signal_loop():
    logging.basicConfig(level=logging.INFO)
    while True:
        for sym in SYMBOLS:
            for tf in INTERVALS:
                try:
                    df = tv.get_hist(sym, tf, n_bars=BARS)
                    if df.empty:
                        logging.warning(f"{sym}-{tf.value}: Veri yok")
                        continue

                    sigs = generate_signal(df)
                    if not sigs:
                        continue

                    ts, sig = sigs[-1]
                    key = f"{sym}_{tf.value}"
                    if last_signals.get(key) != sig:
                        last_signals[key] = sig
                        msg = (
                            f"📊 *Sinyal Geldi!*\n"
                            f"*Coin:* `{sym}`\n"
                            f"*Zaman:* `{tf.value}`\n"
                            f"*Sinyal:* `{sig}`\n"
                            f"🕒 {ts.strftime('%Y-%m-%d %H:%M')}"
                        )
                        await bot.send_message(chat_id=CHANNEL_ID, text=msg, parse_mode="Markdown")
                except Exception as e:
                    logging.error(f"{sym}-{tf.value}: HATA → {e}")
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(run_signal_loop())
