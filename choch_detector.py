# choch_detector.py
import pandas as pd

def detect_choch(df: pd.DataFrame):
    choch_signals = []
    swing_high = swing_low = None

    for i in range(3, len(df)):
        prev = df.iloc[i-1]; curr = df.iloc[i]
        highs = df['high'].iloc[i-3:i]
        lows  = df['low'].iloc[i-3:i]

        if prev['high'] == highs.max():
            swing_high = prev['high']
        if prev['low']  == lows.min():
            swing_low = prev['low']

        if swing_high and curr['close'] > swing_high:
            choch_signals.append((df.index[i], 'CHoCH_UP'))
            swing_high = swing_low = None
        elif swing_low and curr['close'] < swing_low:
            choch_signals.append((df.index[i], 'CHoCH_DOWN'))
            swing_low = swing_high = None

    return choch_signals
