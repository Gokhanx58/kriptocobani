import asyncio
from datetime import datetime
from analyzer import analyze
from tvdatafeed import TvDatafeed, Interval
import telegram

# Telegram bot ayarları
BOT_TOKEN = '7677308602:AAHH7vloPaQ7PqgFdBnJ2DKYy6sjJ5iqaYE'
CHANNEL_ID = '@GokriptoHan'
bot = telegram.Bot(token=BOT_TOKEN)

# TradingView login
tv = TvDatafeed(username='marsticaret1', password='8690Yn678690')

# Sadece bu semboller analiz edilir
SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'SUIUSDT']
INTERVALS = [Interval.MIN_1, Interval.MIN_5]

last_signals = {}

async def run_signal_loop():
    while True:
        for symbol in SYMBOLS:
            for interval in INTERVALS:
                df = tv.get_hist(symbol=symbol, interval=interval, n_bars=bars)
                if df is None or df.empty:
                    continue

                results = analyze(df)
                if results:
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

        await asyncio.sleep(60)
