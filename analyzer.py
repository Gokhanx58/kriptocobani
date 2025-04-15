from tvdatafeed import TvDatafeed, Interval
import pandas as pd

# TradingView login bilgileri (giriş yapmaya gerek yoksa boş bırakılabilir)
tv = TvDatafeed()

# Kayma toleransı (örnek: 0.002 = %0.2 farkla sinyal geçerli kabul edilir)
TOLERANS = 0.002

# Önceki sinyallerin tutulduğu yer
previous_signals = {}

def get_current_signal(df):
    last = df.iloc[-1]
    labels = [str(last.get(col, "")).lower() for col in df.columns]

    if "long" in labels and "order" in str(labels) and "fvg" in str(labels):
        return "GÜÇLÜ AL"
    elif "long" in labels:
        return "AL"
    elif "short" in labels and "order" in str(labels) and "fvg" in str(labels):
        return "GÜÇLÜ SAT"
    elif "short" in labels:
        return "SAT"
    return "BEKLE"

def analyze_signals(symbol, interval):
    try:
        # Veriyi al
        data = tv.get_hist(symbol=symbol, exchange='BINANCE', interval=Interval(interval), n_bars=250)
        if data is None or data.empty:
            print(f"[Veri] {symbol}-{interval}m verisi alınamadı.")
            return None, None, None

        # Son fiyat bilgisi
        entry_price = float(data['close'].iloc[-2])
        current_price = float(data['close'].iloc[-1])

        signal = get_current_signal(data)
        key = f"{symbol}_{interval}"

        if key not in previous_signals:
            previous_signals[key] = signal
            return signal, entry_price, current_price

        # Sinyal değiştiyse "işlem kapat" ve yeni sinyal gönder
        if previous_signals[key] != signal and signal != "BEKLE":
            old_signal = previous_signals[key]
            previous_signals[key] = signal
            return f"KAPAT → {old_signal}", entry_price, current_price  # Önce işlem kapat
        elif signal != "BEKLE":
            return signal, entry_price, current_price
        return None, None, None

    except Exception as e:
        print(f"[Analyzer] Hata: {e}")
        return None, None, None
