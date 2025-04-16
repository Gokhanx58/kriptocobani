import pandas as pd

def detect_fvg(df: pd.DataFrame):
    df = df.copy()
    fvg_zones = []

    for i in range(2, len(df)):
        prev = df.iloc[i - 2]
        mid = df.iloc[i - 1]
        curr = df.iloc[i]
        if mid['low'] > prev['high'] and mid['low'] > curr['high']:
            fvg_zones.append((df.index[i - 1], 'FVG_DOWN', mid['low'], prev['high']))
        elif mid['high'] < prev['low'] and mid['high'] < curr['low']:
            fvg_zones.append((df.index[i - 1], 'FVG_UP', mid['high'], prev['low']))
    return fvg_zones
