import pandas as pd
import logging

def detect_fvg_zones(df: pd.DataFrame, lookback:int=30):
    fvg = []
    for i in range(2, len(df)):
        h2 = df['high'].iat[i-2]; l1 = df['low'].iat[i-1]; l0 = df['low'].iat[i]
        if l1 > h2:
            fvg.append((df.index[i], 'FVG_DOWN', h2, l1))
        elif df['high'].iat[i-1] < l0:
            fvg.append((df.index[i], 'FVG_UP', df['high'].iat[i-1], l0))

    logging.warning(f"FVG ZONES: {fvg}")
    return fvg
