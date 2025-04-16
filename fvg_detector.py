import pandas as pd

def detect_fvg_zones(df: pd.DataFrame, lookback: int = 30):
    fvg_zones = []

    for i in range(2, len(df)):
        high_2 = df['high'].iloc[i - 2]
        low_0 = df['low'].iloc[i]

        if df['low'].iloc[i - 1] > high_2:
            # Fair Value Gap (Boşluk) oluşmuş: düşüş yönlü
            fvg_zones.append({
                'timestamp': df.index[i],
                'direction': 'down',
                'gap_high': df['low'].iloc[i - 1],
                'gap_low': high_2
            })

        elif df['high'].iloc[i - 1] < low_0:
            # Fair Value Gap (Boşluk) oluşmuş: yükseliş yönlü
            fvg_zones.append({
                'timestamp': df.index[i],
                'direction': 'up',
                'gap_high': low_0,
                'gap_low': df['high'].iloc[i - 1]
            })

    return fvg_zones
