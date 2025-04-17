import pandas as pd
import logging

def detect_choch(df: pd.DataFrame):
    choch_signals = []
    swing_high = None
    swing_low = None

    for i in range(3, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        if df['high'].iloc[i-3:i].max() == prev['high']:
            swing_high = prev['high']
            swing_high_time = df.index[i - 1]
            logging.debug(f"Swing high: {swing_high} @ {swing_high_time}")

        if df['low'].iloc[i-3:i].min() == prev['low']:
            swing_low = prev['low']
            swing_low_time = df.index[i - 1]
            logging.debug(f"Swing low: {swing_low} @ {swing_low_time}")

        if swing_high and curr['close'] > swing_high:
            signal_time = df.index[i]
            choch_signals.append((signal_time, 'CHoCH_UP'))
            logging.info(f"CHoCH_UP @ {signal_time}")
            swing_high = swing_low = None

        elif swing_low and curr['close'] < swing_low:
            signal_time = df.index[i]
            choch_signals.append((signal_time, 'CHoCH_DOWN'))
            logging.info(f"CHoCH_DOWN @ {signal_time}")
            swing_high = swing_low = None

    return choch_signals
