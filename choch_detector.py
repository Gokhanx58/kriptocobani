# choch_detector.py
import logging
import pandas as pd

def detect_choch(df: pd.DataFrame):
    choch = []
    swing_high = swing_low = None

    for i in range(3, len(df)):
        prev, curr = df.iloc[i-1], df.iloc[i]
        if df['high'].iloc[i-3:i].max() == prev['high']:
            swing_high = prev['high']
        if df['low'].iloc[i-3:i].min() == prev['low']:
            swing_low = prev['low']

        if swing_high and curr['close'] > swing_high:
            choch.append((df.index[i], 'CHoCH_UP'))
            swing_high = swing_low = None
        elif swing_low and curr['close'] < swing_low:
            choch.append((df.index[i], 'CHoCH_DOWN'))
            swing_high = swing_low = None

    logging.debug(f"CHOCH: {choch}")
    return choch
