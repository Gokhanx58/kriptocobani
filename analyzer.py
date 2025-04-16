from tvdatafeed import TvDatafeed, Interval
from config import SYMBOLS, INTERVALS, TOLERANCE
from utils import round_to_nearest
from send_message import send_signal_to_channel
import datetime

# TV Login
tv = TvDatafeed(username="marsticaret1", password="8690Yn678690")

last_signal_state = {}

def analyze_signals():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            try:
                df = tv.get_hist(symbol=symbol, exchange='BINANCE', interval=Interval[interval], n_bars=300)
                if df is None or df.empty or len(df) < 10:
                    continue

                df.dropna(inplace=True)
                df.reset_index(inplace=True)

                last_close = df['close'].iloc[-1]
                signal_price = df['close'].iloc[-2]

                choch_signal = check_choch(df)
                ob_signal = check_order_block(df)
                fvg_signal = check_fvg(df)

                signal_strength = [choch_signal, ob_signal, fvg_signal].count("AL") - [choch_signal, ob_signal, fvg_signal].count("SAT")

                if signal_strength >= 2:
                    signal = "Güçlü AL"
                elif signal_strength == 1:
                    signal = "AL"
                elif signal_strength <= -2:
                    signal = "Güçlü SAT"
                elif signal_strength == -1:
                    signal = "SAT"
                else:
                    signal = "BEKLE"

                key = f"{symbol}_{interval}"
                previous_signal = last_signal_state.get(key)

                if signal != "BEKLE" and signal != previous_signal:
                    last_signal_state[key] = signal
                    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

                    await send_signal_to_channel(symbol, interval, signal, signal_price, last_close)

            except Exception as e:
                print(f"Hata: {e}")

def check_choch(df):
    return "AL" if df['close'].iloc[-1] > df['close'].iloc[-2] else "SAT"

def check_order_block(df):
    return "AL" if df['low'].iloc[-1] > df['low'].iloc[-2] else "SAT"

def check_fvg(df):
    return "AL" if df['high'].iloc[-1] > df['high'].iloc[-2] else "SAT"
