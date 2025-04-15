# analyzer.py

from tvdatafeed import TvDatafeed, Interval
from utils import round_to_nearest
import datetime

# TradingView login bilgileriniz (Render icin cookies ile calisiyor olacak)
tv = TvDatafeed(username=None, password=None)

# Kayma toleransı (örneğin 0.002 → %0.2)
SLIPPAGE = 0.002

# Önceki sinyalleri saklamak için (sembol/zaman dilimi bazlı)
last_signals = {}

def detect_signal(df):
    """
    Mxwll Suite sinyal kurallarına göre temel sinyal oluşturucu.
    Sadece CHoCH + Order Block + FVG bir aradaysa sinyal üretilecek.
    Bu kısmı daha sonra geliştirilebilir hale getirdik.
    """
    # Simülasyon: son 5 mumda CHoCH, Order Block ve FVG varlığına bakıyoruz (sadece örnek)
    if len(df) < 5:
        return "BEKLE", 0.0

    row = df.iloc[-1]

    # Göstergesel şartlar burada kontrol edilir
    choch = row.get("choch", False)
    order_block = row.get("order_block", False)
    fvg = row.get("fvg", False)

    if choch and order_block and fvg:
        if row["close"] > row["open"]:
            return "GÜÇLÜ AL", row["close"]
        else:
            return "GÜÇLÜ SAT", row["close"]

    if (choch and order_block) or (order_block and fvg):
        if row["close"] > row["open"]:
            return "AL", row["close"]
        else:
            return "SAT", row["close"]

    return "BEKLE", row["close"]

def analyze_signals(symbol, interval):
    """
    Belirtilen coin ve zaman dilimine gore analiz yapar.
    """
    try:
        tv_interval = Interval.in_1_minute if interval == "1m" else Interval.in_5_minute
        df = tv.get_hist(symbol=symbol, exchange="BINANCE", interval=tv_interval, n_bars=100)
        if df is None or df.empty:
            print(f"[!] Veri alinamadi: {symbol}-{interval}")
            return None

        # Örnek sütunları simüle edelim (çünkü TradingView Mxwll Suite verisi pine script üzerinden çekilemiyor)
        df["choch"] = df["close"].diff().abs() > 5
        df["order_block"] = df["close"].rolling(3).mean() > df["open"]
        df["fvg"] = (df["high"] - df["low"]).rolling(3).mean() > 10

        signal, signal_price = detect_signal(df)
        now_price = df.iloc[-1]["close"]

        # Önceki sinyal ile karşılaştır
        key = f"{symbol}_{interval}"
        previous_signal = last_signals.get(key, (None, None))

        if previous_signal[0] and previous_signal[0] != signal and signal != "BEKLE":
            # Sinyal değişimi varsa
            last_signals[key] = (signal, signal_price)
            return {
                "symbol": symbol,
                "interval": interval,
                "signal": signal,
                "signal_price": signal_price,
                "now_price": now_price,
                "close_last": previous_signal[0]
            }

        elif previous_signal[0] != signal and signal != "BEKLE":
            last_signals[key] = (signal, signal_price)
            return {
                "symbol": symbol,
                "interval": interval,
                "signal": signal,
                "signal_price": signal_price,
                "now_price": now_price,
                "close_last": None
            }

        return None

    except Exception as e:
        print(f"❌ {symbol} {interval} analiz hatası: {e}")
        return None
