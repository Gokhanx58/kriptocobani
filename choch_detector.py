import pandas as pd
import logging

def detect_choch(df: pd.DataFrame):
    choch_signals = []
    swing_high = swing_low = None

    for i in range(3, len(df)):
        prev, curr = df.iloc[i - 1], df.iloc[i]
        # swing high
        if df['high'].iloc[i-3:i].max() == prev['high']:
            swing_high, swing_high_time = prev['high'], df.index[i-1]
        # swing low
        if df['low'].iloc[i-3:i].min() == prev['low']:
            swing_low, swing_low_time = prev['low'], df.index[i-1]

        if swing_high and curr['close'] > swing_high:
            choch_signals.append((df.index[i], 'CHoCH_UP'))
            swing_high = swing_low = None
        elif swing_low and curr['close'] < swing_low:
            choch_signals.append((df.index[i], 'CHoCH_DOWN'))
            swing_high = swing_low = None

    logging.debug(f"CHOCH: {choch_signals}")
    return choch_signals
