from tvDatafeed import TvDatafeed
from ta.momentum import RSIIndicator
import pandas as pd

def analyze_signals(symbol, interval):
    tv = TvDatafeed()
    try:
        df = tv.get_hist(symbol=symbol, exchange='BINANCE', interval=interval, n_bars=100)
        df.dropna(inplace=True)
        df['rsi'] = RSIIndicator(close=df['close'], window=14).rsi()

        if df['rsi'].iloc[-1] < 30:
            return "AL"
        elif df['rsi'].iloc[-1] > 70:
            return "SAT"
        else:
            return "BEKLE"
    except Exception as e:
        print(f"Analiz hatası ({symbol}-{interval}): {e}")
        return None
