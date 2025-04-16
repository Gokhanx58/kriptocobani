# main.py
import asyncio
from tvdatafeed import TvDatafeed, Interval
from signal_generator import generate_signal
import telegram

BOT_TOKEN = '7677308602:AAHH7vloPaQ7PqgFdBnJ2DKYy6sjJ5iqaYE'
CHANNEL_ID = '@GokriptoHan'
bot = telegram.Bot(token=BOT_TOKEN)

# TradingView login
tv = TvDatafeed(username='marsticaret1', password='8690Yn678690')

SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'SUIUSDT']
INTERVALS = [Interval.MIN_1, Interval.MIN_5]

async def run():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            try:
                df = tv.get_hist(symbol=symbol, interval=interval, n_bars=100)
                if df is None or df.empty:
                    continue

                final_signals = generate_signal(df)
                if final_signals:
                    for signal_time, symbol, tf, signal in final_signals:
                        message = (
                            f"\n📊 *Sinyal Geldi!*\n"
                            f"*Sembol:* `{symbol}`\n"
                            f"*Zaman Dilimi:* `{tf}`\n"
                            f"*Sinyal:* `{signal}`\n"
                            f"🕒 {signal_time}"
                        )
                        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")
            except Exception as e:
                print(f"HATA ({symbol}-{interval}):", e)

if __name__ == '__main__':
    asyncio.run(run())


# signal_generator.py
import logging
from choch_detector import detect_choch
from order_block_detector import detect_order_blocks
from fvg_detector import detect_fvg

def generate_signal(df):
    choch_signals = detect_choch(df)
    order_blocks = detect_order_blocks(df)
    fvg_zones = detect_fvg(df)

    logging.warning(f"CHOCH: {choch_signals}")
    logging.warning(f"ORDER BLOCKS: {order_blocks}")
    logging.warning(f"FVG ZONES: {fvg_zones}")

    final_signals = []
    for ts, choch_signal in choch_signals:
        ob_match = any(abs((ts - ob[0]).total_seconds()) < 180 for ob in order_blocks)
        fvg_match = any(abs((ts - fvg[0]).total_seconds()) < 180 for fvg in fvg_zones)

        if ob_match and fvg_match:
            symbol = df['symbol'][0] if 'symbol' in df.columns else 'UNKNOWN'
            tf = df['interval'][0] if 'interval' in df.columns else 'UNKNOWN'
            final_signals.append((ts.strftime('%Y-%m-%d %H:%M'), symbol, tf, 'AL' if 'UP' in choch_signal else 'SAT'))

    logging.warning(f"FINAL SIGNALS: {final_signals}")
    return final_signals
