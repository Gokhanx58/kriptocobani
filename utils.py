from tvDatafeed import TvDatafeed
from ta.momentum import RSIIndicator
import pandas as pd

tv = TvDatafeed()

def get_indicator_data(symbol, interval):
    try:
        df = tv.get_hist(symbol=symbol, exchange='MEXC', interval=interval, n_bars=100)

        if df is None or len(df) < 30:
            return "BEKLE", "BEKLE"

        # RSI hesaplama
        rsi = RSIIndicator(close=df['close'], window=14).rsi()
        last_rsi = rsi.iloc[-1]

        if last_rsi > 70:
            rsi_signal = "SAT"
        elif last_rsi < 30:
            rsi_signal = "AL"
        else:
            rsi_signal = "BEKLE"

        # RMI yerine mum rengine dayalı basit momentum tahmini (örnek)
        last_close = df['close'].iloc[-1]
        prev_close = df['close'].iloc[-2]

        if last_close > prev_close:
            rmi_signal = "AL"
        elif last_close < prev_close:
            rmi_signal = "SAT"
        else:
            rmi_signal = "BEKLE"

        return rsi_signal, rmi_signal

    except Exception as e:
        print(f"Veri alınırken hata oluştu: {e}")
        return "BEKLE", "BEKLE"
