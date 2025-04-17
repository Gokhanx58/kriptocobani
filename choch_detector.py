import pandas as pd
import logging

def detect_choch(df: pd.DataFrame):
    choch_signals = []
    swing_high = swing_low = None

    for i in range(3, len(df)):
        prev = df.iloc[i-1]
        curr = df.iloc[i]

        # Swing High / Low tespiti
        window_high = df['high'].iloc[i-3:i].max()
        window_low  = df['low'].iloc[i-3:i].min()

        if prev['high'] == window_high:
            swing_high = prev['high']
            swing_high_time = df.index[i-1]
            logging.debug(f"Pivot High at {swing_high_time}: {swing_high}")

        if prev['low'] == window_low:
            swing_low = prev['low']
            swing_low_time = df.index[i-1]
            logging.debug(f"Pivot Low  at {swing_low_time}: {swing_low}")

        # Fiyat kırılımları
        if swing_high and curr['close'] > swing_high:
            logging.info(f"CHoCH_UP at {df.index[i]}: close {curr['close']} > swing_high {swing_high}")
            choch_signals.append((df.index[i], 'CHoCH_UP'))
            swing_high = swing_low = None

        elif swing_low and curr['close'] < swing_low:
            logging.info(f"CHoCH_DOWN at {df.index[i]}: close {curr['close']} < swing_low {swing_low}")
            choch_signals.append((df.index[i], 'CHoCH_DOWN'))
            swing_high = swing_low = None

    logging.warning(f"CHOCH: {choch_signals}")
    return choch_signals
