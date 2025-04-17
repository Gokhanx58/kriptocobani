import pandas as pd
import logging

def detect_order_blocks(df: pd.DataFrame, choch_signals):
    obs = []
    for ts, direction in choch_signals:
        if ts not in df.index:
            continue
        idx = df.index.get_loc(ts)
        look = df.iloc[idx+1:idx+4]
        if look.empty: continue

        if direction == "CHoCH_UP":
            # bekleyen ilk kırmızı mum
            for t, row in look.iterrows():
                if row.close < row.open:
                    obs.append((t, "OB_SHORT", row.high, row.low))
                    break
        else:  # CHoCH_DOWN
            for t, row in look.iterrows():
                if row.close > row.open:
                    obs.append((t, "OB_LONG", row.high, row.low))
                    break

    logging.debug(f"ORDER BLOCKS: {obs}")
    return obs
