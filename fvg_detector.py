import pandas as pd
import logging

def detect_fvg_zones(df: pd.DataFrame):
    fvgs = []
    for i in range(2, len(df)):
        high_2, mid_low, low_0 = df.high.iat[i-2], df.low.iat[i-1], df.low.iat[i]
        if mid_low > high_2:
            fvgs.append((df.index[i], "FVG_DOWN", mid_low, high_2))
        else:
            high_1 = df.high.iat[i-1]
            if high_1 < low_0:
                fvgs.append((df.index[i], "FVG_UP", low_0, high_1))
    logging.debug(f"FVG ZONES: {fvgs}")
    return fvgs
