from tvdatafeed import TvDatafeed, Interval
import pandas as pd
import datetime
from config import SYMBOLS, INTERVALS, TOLERANCE
from send_message import send_telegram_message
from utils import round_to_nearest

tv = TvDatafeed()
last_signal_state = {}

def check_choch(df):
    return "AL" if df['close'].iloc[-1] > df['close'].iloc[-2] else "SAT"

def check_order_block(df):
    return "AL" if df['low'].iloc[-1] > df['low'].iloc[-2] else "SAT"

def check_fvg(df):
    return "AL" if df['high'].iloc[-1] > df['high'].iloc[-2] else "SAT"

def analyze_signals():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            try:
                df = tv.get_hist(
                    symbol=symbol,
                    exchange='BINANCE',
                    interval=Interval.__members__[interval],
                    n_bars=300
                )

                if df is None or df.empty or len(df) < 10:
                    print(f"⛔ Veri eksik: {symbol} | {interval}")
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

                print(f"📊 {symbol} [{interval}] | Sinyal: {signal} | Önceki: {previous_signal}")

                if signal != "BEKLE" and signal != previous_signal:
                    last_signal_state[key] = signal

                    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

                    message = (
                        f"🪙 Coin: {symbol}\n"
                        f"⏱️ Zaman: {interval}\n"
                        f"📊 Sistem: CHoCH + Order Block + FVG (AL-GÜÇLÜ AL - SAT-GÜÇLÜ SAT)\n"
                        f"📌 Sinyal: ✅ {signal}\n"
                        f"📈 Sinyal Geldiği Fiyat: {round_to_nearest(signal_price, TOLERANCE)}\n"
                        f"💰 Şu Anki Fiyat: {round_to_nearest(last_close, TOLERANCE)}\n"
                        f"⏰ Zaman: {now}"
                    )

                    send_telegram_message(message)

            except Exception as e:
                print(f"🚨 Hata ({symbol}-{interval}): {e}")
