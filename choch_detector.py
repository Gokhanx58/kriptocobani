import pandas as pd
import logging

def detect_choch(df: pd.DataFrame):
    choch_signals = []
    swing_high = None
    swing_low = None
    swing_high_time = None
    swing_low_time = None

    for i in range(3, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        # Swing High
        window_high = df['high'].iloc[i - 3:i]
        if window_high.max() == prev['high']:
            swing_high = prev['high']
            swing_high_time = df.index[i - 1]
            logging.debug(f"Swing high: {swing_high} @ {swing_high_time}")

        # Swing Low
        window_low = df['low'].iloc[i - 3:i]
        if window_low.min() == prev['low']:
            swing_low = prev['low']
            swing_low_time = df.index[i - 1]
            logging.debug(f"Swing low: {swing_low} @ {swing_low_time}")

        # CHoCH up
        if swing_high is not None and curr['close'] > swing_high:
            ts = df.index[i]
            choch_signals.append((ts, "CHoCH_UP"))
            logging.info(f"CHoCH_UP @ {ts}")
            swing_high = swing_low = None

        # CHoCH down
        elif swing_low is not None and curr['close'] < swing_low:
            ts = df.index[i]
            choch_signals.append((ts, "CHoCH_DOWN"))
            logging.info(f"CHoCH_DOWN @ {ts}")
            swing_high = swing_low = None

    return choch_signals
