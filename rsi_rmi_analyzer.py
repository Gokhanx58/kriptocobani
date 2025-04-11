from tvDatafeed import TvDatafeed
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def analyze_signals(symbol, interval, manual=False, chat_id=None):
    try:
        tv = TvDatafeed()
        bars = tv.get_hist(symbol=symbol, exchange='BINANCE', interval=interval, n_bars=100)

        if bars is None or bars.empty:
            raise Exception("Veri alınamadı.")

        close = bars['close']
        rsi = close.pct_change().rolling(window=14).std()
        rmi = close.rolling(window=14).mean()

        last_rsi = rsi.iloc[-1]
        last_rmi = rmi.iloc[-1]

        if last_rsi > last_rmi:
            return f"📈 AL sinyali: RSI ({last_rsi:.2f}) > RMI ({last_rmi:.2f})"
        elif last_rsi < last_rmi:
            return f"📉 SAT sinyali: RSI ({last_rsi:.2f}) < RMI ({last_rmi:.2f})"
        else:
            return "⏸️ BEKLE sinyali"

    except Exception as e:
        logging.error(f"Veri alınamadı: {e}")
        return f"Hata oluştu: {e}"
