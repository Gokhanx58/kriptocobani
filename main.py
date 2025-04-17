# main.py
import asyncio
import logging
from binance_client import get_klines
from signal_generator import generate_signal
import telegram

# Telegram bot ayarları
BOT_TOKEN = "7677308602:AAHH7vloPaQ7z3oCKrettxY7v1u1cSvcjCnPflkvM0Pst3E="
CHANNEL_ID = "@GokriptoHan"
bot = telegram.Bot(token=BOT_TOKEN)

# Semboller ve zaman dilimleri
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]
INTERVALS = ["1m", "5m"]
BARS     = 200

last_signals = {}

async def run_signal_loop():
    logging.basicConfig(level=logging.INFO)
    while True:
        for symbol in SYMBOLS:
            for interval in INTERVALS:
                try:
                    df = get_klines(symbol, interval, limit=BARS)
                    if df.empty:
                        logging.warning(f"{symbol}-{interval}: Veri yok")
                        continue

                    signals = generate_signal(df)
                    if not signals:
                        continue

                    ts, sig = signals[-1]
                    key = f"{symbol}_{interval}"
                    if last_signals.get(key) != sig:
                        last_signals[key] = sig

                        message = (
                            f"📊 *Sinyal Geldi!*\n"
                            f"*Coin:* `{symbol}`\n"
                            f"*Zaman:* `{interval}`\n"
                            f"*Sistem:* CHoCH + Order Block + FVG\n"
                            f"*Sinyal:* `{sig}`\n"
                            f"🕒 {ts.strftime('%Y-%m-%d %H:%M')}"
                        )
                        await bot.send_message(
                            chat_id=CHANNEL_ID,
                            text=message,
                            parse_mode="Markdown"
                        )
                except Exception as e:
                    logging.error(f"{symbol}-{interval}: HATA → {e}")
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(run_signal_loop())
