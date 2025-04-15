analyzer.py
```python
from tvdatafeed import TvDatafeed, Interval
from utils import round_to_nearest
from telegram_send import send_signal_to_channel

prev_signals = {}

interval_map = {
    1: Interval.in_1_minute,
    5: Interval.in_5_minute
}

tv = TvDatafeed()

def determine_signal(df):
    # Simülasyon amaçlı: son kapanış değerine göre sinyal ver
    last = df.close.iloc[-1]
    prev = df.close.iloc[-2]
    diff = last - prev
    if diff > 0.1:
        return "AL"
    elif diff < -0.1:
        return "SAT"
    return "BEKLE"

async def analyze_signals(symbol, tf):
    interval = interval_map[tf]
    df = tv.get_hist(symbol=symbol, exchange="MEXC", interval=interval, n_bars=50)
    if df is None or df.empty:
        raise ValueError("Veri alınamadı")

    signal = determine_signal(df)
    prev = prev_signals.get((symbol, tf))

    if prev != signal:
        price = df.close.iloc[-2]
        current = df.close.iloc[-1]
        await send_signal_to_channel(symbol, tf, signal, price, current)
        prev_signals[(symbol, tf)] = signal
```
