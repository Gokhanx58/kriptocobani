import pandas as pd
import logging

def detect_fvg_zones(df: pd.DataFrame, choch_signals, lookahead: int = 3):
    fvgs = []
    for ts, direction in choch_signals:
        if ts not in df.index:
            continue
        idx = df.index.get_loc(ts)
        window = df.iloc[idx+1:idx+1+lookahead]
        if window.shape[0] < 2:
            continue

        # basit gap: önceki mumun high/low’u ile sonraki mumun low/high’u arasında boşluk
        prev = window.iloc[0]
        curr = window.iloc[1]

        if direction == "CHoCH_UP":
            # düşüş yönlü gap
            if curr['low'] > prev['high']:
                fvgs.append((window.index[1], "FVG_DOWN", prev['high'], curr['low']))

        else:
            # yükseliş yönlü gap
            if curr['high'] < prev['low']:
                fvgs.append((window.index[1], "FVG_UP", curr['high'], prev['low']))

    logging.debug(f"FVG ZONES: {fvgs}")
    return fvgs
