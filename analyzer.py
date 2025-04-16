from tvdatafeed import TvDatafeed, Interval
import pandas as pd
from send_message import send_signal_to_channel
from config import SYMBOLS, INTERVALS
from utils import round_to_nearest

last_signal_state = {}
tv = TvDatafeed()

async def analyze_signals():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            try:
                df = tv.get_hist(symbol=symbol, exchange='BINANCE', interval=Interval.__members__[interval], n_bars=300)
                if df is None or df.empty or len(df) < 10:
                    continue

                df.dropna(inplace=True)
                df.reset_index(inplace=True)

                last_close = df['close'].iloc[-1]
                signal_price = df['close'].iloc[-2]

                choch_signal = check_choch(df)
                ob_signal = check_order_block(df)
                fvg_signal = check_fvg(df)

                signal_components = [choch_signal, ob_signal, fvg_signal]
                signal_strength = signal_components.count("AL") - signal_components.count("SAT")

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
                previous_signal = last_signal_state.get(key)

                if signal != "BEKLE" and signal != previous_signal:
                    last_signal_state[key] = signal
                    await send_signal_to_channel(symbol, interval, signal, signal_price, last_close)

            except Exception as e:
                print(f"Hata: {e}")

def check_choch(df):
    return "AL" if df['close'].iloc[-1] > df['close'].iloc[-2] else "SAT"

def check_order_block(df):
    return "AL" if df['low'].iloc[-1] > df['low'].iloc[-2] else "SAT"

def check_fvg(df):
    return "AL" if df['high'].iloc[-1] > df['high'].iloc[-2] else "SAT"
