# analyzer.py
from binance_client import get_klines
from signal_generator import generate_signal

def analyze_signals():
    import logging
    from config import SYMBOLS, INTERVALS, BARS
    from telegram_bot import send_telegram

    for symbol in SYMBOLS:
        for interval in INTERVALS:
            df = get_klines(symbol, interval, limit=BARS)
            if df.empty:
                logging.warning(f"{symbol}-{interval}: Veri yok veya hata.")
                continue

            signals = generate_signal(df)
            if signals:
                ts, sig = signals[-1]
                msg = (
                    f"📊 *Sistem:* CHoCH+OB+FVG\n"
                    f"*Sembol:* `{symbol}`\n"
                    f"*Zaman:* `{interval}`\n"
                    f"*Sinyal:* `{sig}`\n"
                    f"🕒 {ts.strftime('%Y-%m-%d %H:%M')}"
                )
                send_telegram(msg)
