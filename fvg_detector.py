import pandas as pd

def detect_fvg(df):
    fvg_zones = []

    for i in range(2, len(df)):
        high_2 = df['high'].iloc[i - 2]
        low_2 = df['low'].iloc[i - 2]
        high_1 = df['high'].iloc[i - 1]
        low_1 = df['low'].iloc[i - 1]
        high_0 = df['high'].iloc[i]
        low_0 = df['low'].iloc[i]

        time = df.index[i]

        # Bullish FVG (Up Gap)
        if low_0 > high_2:
            fvg_zones.append((time, 'FVG_UP', high_2, low_0))

        # Bearish FVG (Down Gap)
        elif high_0 < low_2:
            fvg_zones.append((time, 'FVG_DOWN', high_0, low_2))

    return fvg_zones
