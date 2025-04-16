import pandas as pd

def detect_fvg(df: pd.DataFrame):
    fvg_zones = []

    for i in range(2, len(df)):
        # FVG_DOWN: önceki iki mumun low'u > son mumun high'ı
        if df['low'].iloc[i - 2] > df['high'].iloc[i - 1] and df['low'].iloc[i - 1] > df['high'].iloc[i]:
            ts = df.index[i]
            fvg_zones.append((ts, 'FVG_DOWN'))

        # FVG_UP: önceki iki mumun high'ı < son mumun low'u
        elif df['high'].iloc[i - 2] < df['low'].iloc[i - 1] and df['high'].iloc[i - 1] < df['low'].iloc[i]:
            ts = df.index[i]
            fvg_zones.append((ts, 'FVG_UP'))

    print("Tespit edilen FVG'ler:", fvg_zones)
    return fvg_zones
