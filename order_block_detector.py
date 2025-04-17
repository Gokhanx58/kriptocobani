# order_block_detector.py
import logging
import pandas as pd

def detect_order_blocks(df: pd.DataFrame, choch_signals):
    obs = []
    for ts, direction in choch_signals:
        if ts not in df.index: continue
        window = df.loc[ts:].iloc[1:4]
        if window.empty: continue

        if direction == "CHoCH_UP":
            for t, c in window.iterrows():
                if c['close'] < c['open']:
                    obs.append((t, "OB_SHORT", c['high'], c['low']))
                    break
        else:  # CHoCH_DOWN
            for t, c in window.iterrows():
                if c['close'] > c['open']:
                    obs.append((t, "OB_LONG", c['high'], c['low']))
                    break

    logging.debug(f"ORDER BLOCKS: {obs}")
    return obs
