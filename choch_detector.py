import pandas as pd

def detect_choch(df: pd.DataFrame):
    """
    CHoCH (Change of Character) tespiti yapar.
    Fiyatın önceki swing high/low seviyelerine göre yön değiştirdiği noktaları bulur.

    :param df: OHLCV içeren DataFrame (timestamp index'li)
    :return: CHoCH sinyalleri listesi: [(timestamp, 'CHoCH_UP' | 'CHoCH_DOWN')]
    """

    choch_signals = []
    swing_high = None
    swing_low = None

    for i in range(3, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        # Swing High tespiti: önceki 3 barın en yükseği
        if df['high'].iloc[i - 3:i].max() == prev['high']:
            swing_high = prev['high']
            swing_high_time = df.index[i - 1]

        # Swing Low tespiti: önceki 3 barın en düşüğü
        if df['low'].iloc[i - 3:i].min() == prev['low']:
            swing_low = prev['low']
            swing_low_time = df.index[i - 1]

        # CHoCH_UP: fiyat swing high seviyesini kırdıysa
        if swing_high and curr['close'] > swing_high:
            choch_signals.append((df.index[i], 'CHoCH_UP'))
            swing_high = None  # reset
            swing_low = None

        # CHoCH_DOWN: fiyat swing low seviyesini kırdıysa
        elif swing_low and curr['close'] < swing_low:
            choch_signals.append((df.index[i], 'CHoCH_DOWN'))
            swing_low = None  # reset
            swing_high = None

    return choch_signals
