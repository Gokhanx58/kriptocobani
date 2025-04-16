from config import SYMBOLS, INTERVALS
from tvdatafeed import TvDatafeed, Interval
from telegram_send import send_signal_to_channel

tv = TvDatafeed()

last_signal_state = {}

def get_signal_strength(choch, ob, fvg):
    return [choch, ob, fvg].count("AL") - [choch, ob, fvg].count("SAT")

async def analyze_signals():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            try:
                df = tv.get_hist(symbol=symbol, exchange='BINANCE', interval=Interval.__members__[interval], n_bars=100)
                if df is None or df.empty or len(df) < 5:
                    continue

                df.dropna(inplace=True)
                df.reset_index(inplace=True)

                signal_price = df['close'].iloc[-2]
                last_close = df['close'].iloc[-1]

                choch = "AL" if df['close'].iloc[-1] > df['close'].iloc[-2] else "SAT"
                ob = "AL" if df['low'].iloc[-1] > df['low'].iloc[-2] else "SAT"
                fvg = "AL" if df['high'].iloc[-1] > df['high'].iloc[-2] else "SAT"

                signal_strength = get_signal_strength(choch, ob, fvg)

                if signal_strength >= 2:
                    signal = "GÜÇLÜ AL"
                elif signal_strength == 1:
                    signal = "AL"
                elif signal_strength <= -2:
                    signal = "GÜÇLÜ SAT"
                elif signal_strength == -1:
                    signal = "SAT"
                else:
                    signal = "BEKLE"

                key = f"{symbol}_{interval}"
                if signal != "BEKLE" and signal != last_signal_state.get(key):
                    last_signal_state[key] = signal
                    await send_signal_to_channel(symbol, interval, signal, signal_price, last_close)

            except Exception as e:
                print(f"[{symbol}-{interval}] Hata: {e}")
