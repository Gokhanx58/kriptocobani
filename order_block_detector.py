import pandas as pd
import logging

def detect_order_blocks(df: pd.DataFrame, choch_signals):
    obs = []
    for ts, direction in choch_signals:
        if ts not in df.index: continue
        idx = df.index.get_loc(ts)
        window = df.iloc[idx+1:idx+4]
        if window.empty: continue

        if direction == 'CHoCH_UP':
            for c in window.itertuples():
                if c.close < c.open:
                    obs.append((c.Index, 'OB_SHORT', c.high, c.low))
                    break
        else:  # CHoCH_DOWN
            for c in window.itertuples():
                if c.close > c.open:
                    obs.append((c.Index, 'OB_LONG', c.high, c.low))
                    break

    logging.warning(f"ORDER BLOCKS: {obs}")
    return obs
