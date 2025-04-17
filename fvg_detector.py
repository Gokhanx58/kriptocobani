import pandas as pd

def detect_fvg_zones(df: pd.DataFrame, lookback: int = 30):
    """
    (timestamp, 'FVG_DOWN' | 'FVG_UP', gap_high, gap_low) tuple'ları döner.
    """
    fvg_zones = []

    for i in range(2, len(df)):
        # önce 2 bar geriye bakıp gap kriterini kontrol edelim
        if df['low'].iloc[i-1] > df['high'].iloc[i-2]:
            ts = df.index[i]
            high = df['low'].iloc[i-1]
            low  = df['high'].iloc[i-2]
            fvg_zones.append((ts, 'FVG_DOWN', high, low))

        elif df['high'].iloc[i-1] < df['low'].iloc[i]:
            ts = df.index[i]
            high = df['low'].iloc[i]
            low  = df['high'].iloc[i-1]
            fvg_zones.append((ts, 'FVG_UP', high, low))

    return fvg_zones
