import pandas as pd

def detect_fvg(df, min_gap_percent=0.1):
    fvg_zones = []
    for i in range(2, len(df)):
        high_0 = df['high'].iloc[i - 2]
        low_1 = df['low'].iloc[i - 1]
        low_2 = df['low'].iloc[i - 2]
        high_1 = df['high'].iloc[i - 1]

        # FVG Up (boşluk yukarı yönlü)
        if low_1 > high_0:
            gap_size = low_1 - high_0
            gap_percent = (gap_size / high_0) * 100
            if gap_percent >= min_gap_percent:
                fvg_zones.append((df.index[i], 'FVG_UP', high_0, low_1))

        # FVG Down (boşluk aşağı yönlü)
        if high_1 < low_2:
            gap_size = low_2 - high_1
            gap_percent = (gap_size / low_2) * 100
            if gap_percent >= min_gap_percent:
                fvg_zones.append((df.index[i], 'FVG_DOWN', high_1, low_2))

    return fvg_zones
