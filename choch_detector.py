import pandas as pd

def detect_structure(df: pd.DataFrame):
    df = df.copy()
    df['HH'] = (df['high'] > df['high'].shift(1)) & (df['high'] > df['high'].shift(-1))
    df['LL'] = (df['low'] < df['low'].shift(1)) & (df['low'] < df['low'].shift(-1))
    return df

def detect_choch(df: pd.DataFrame):
    df = detect_structure(df)
    choch_signals = []
    trend = None

    for i in range(2, len(df)):
        row = df.iloc[i]
        if trend == 'down' and row['HH']:
            choch_signals.append((df.index[i], 'CHoCH_UP'))
            trend = 'up'
        elif trend == 'up' and row['LL']:
            choch_signals.append((df.index[i], 'CHoCH_DOWN'))
            trend = 'down'
        elif trend is None:
            if row['HH']:
                trend = 'up'
            elif row['LL']:
                trend = 'down'
    return choch_signals
