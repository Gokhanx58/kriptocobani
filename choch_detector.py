import pandas as pd

def detect_choch(df):
    df = df.copy()
    choch_signals = []

    df['high_shift'] = df['high'].shift(1)
    df['low_shift'] = df['low'].shift(1)
    df['close_shift'] = df['close'].shift(1)

    structure = None  # Başlangıç yönü bilinmiyor

    for i in range(2, len(df)):
        prev_high = df.iloc[i - 1]['high']
        prev_low = df.iloc[i - 1]['low']
        current_close = df.iloc[i]['close']

        # İlk yönü belirle (yukarı mı aşağı mı gidiyoruz)
        if structure is None:
            if df.iloc[i]['high'] > df.iloc[i - 2]['high']:
                structure = "HIGH"
            elif df.iloc[i]['low'] < df.iloc[i - 2]['low']:
                structure = "LOW"
            continue

        # CHoCH aşağı yönlü
        if structure == "HIGH" and df.iloc[i]['low'] < df.iloc[i - 2]['low']:
            choch_signals.append((df.index[i], "CHoCH_DOWN"))
            structure = "LOW"

        # CHoCH yukarı yönlü
        elif structure == "LOW" and df.iloc[i]['high'] > df.iloc[i - 2]['high']:
            choch_signals.append((df.index[i], "CHoCH_UP"))
            structure = "HIGH"

    return choch_signals
