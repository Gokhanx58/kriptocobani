import pandas as pd
import logging

def detect_fvg_zones(df: pd.DataFrame, lookback: int = 30):
    fvg_zones = []
    for i in range(2, len(df)):
        h2 = df['high'].iloc[i-2]
        l1 = df['low'].iloc[i-1]
        h1 = df['high'].iloc[i-1]
        l0 = df['low'].iloc[i]
        if l1 > h2:
            t = df.index[i]
            fvg_zones.append((t, 'FVG_DOWN', l1, h2))
            logging.info(f"FVG_DOWN @ {t}")
        elif h1 < l0:
            t = df.index[i]
            fvg_zones.append((t, 'FVG_UP', l0, h1))
            logging.info(f"FVG_UP @ {t}")
    logging.debug(f"FVG ZONES: {fvg_zones}")
    return fvg_zones
