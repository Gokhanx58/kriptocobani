# fvg_detector.py
import logging
import pandas as pd

def detect_fvg_zones(df: pd.DataFrame, choch_signals, lookahead: int = 3):
    fvgs = []
    for ts, direction in choch_signals:
        if ts not in df.index: continue
        window = df.loc[ts:].iloc[1:1+lookahead]
        if len(window) < 2: continue

        prev, curr = window.iloc[0], window.iloc[1]
        if direction == "CHoCH_UP" and curr['low'] > prev['high']:
            fvgs.append((window.index[1], "FVG_DOWN", prev['high'], curr['low']))
        elif direction == "CHoCH_DOWN" and curr['high'] < prev['low']:
            fvgs.append((window.index[1], "FVG_UP", curr['high'], prev['low']))

    logging.debug(f"FVG ZONES: {fvgs}")
    return fvgs
