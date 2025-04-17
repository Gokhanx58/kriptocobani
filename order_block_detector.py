import pandas as pd
import logging

def detect_order_blocks(df: pd.DataFrame, choch_signals):
    obs = []
    for ts, direction in choch_signals:
        if ts not in df.index:
            continue
        idx = df.index.get_loc(ts)
        window = df.iloc[idx+1:idx+4]
        if window.empty:
            continue

        if direction == "CHoCH_UP":
            # OB SHORT: kırmızı mum
            for t, candle in window.iterrows():
                if candle['close'] < candle['open']:
                    obs.append((t, "OB_SHORT", candle['high'], candle['low']))
                    break

        else:  # CHoCH_DOWN
            # OB LONG: yeşil mum
            for t, candle in window.iterrows():
                if candle['close'] > candle['open']:
                    obs.append((t, "OB_LONG", candle['high'], candle['low']))
                    break

    logging.debug(f"ORDER BLOCKS: {obs}")
    return obs
