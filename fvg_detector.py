import pandas as pd
from typing import List, Tuple

def detect_fvg(df: pd.DataFrame) -> List[Tuple[pd.Timestamp, str]]:
    fvg_signals = []
    
    # FVG: Fair Value Gap, body gap mantığına göre tespit yapılır
    for i in range(2, len(df)):
        prev2_high = df['high'].iloc[i - 2]
        prev2_low = df['low'].iloc[i - 2]
        prev1_high = df['high'].iloc[i - 1]
        prev1_low = df['low'].iloc[i - 1]
        curr_open = df['open'].iloc[i]
        curr_close = df['close'].iloc[i]
        curr_time = df.index[i]

        # Gap up: önceki 2 mumun en düşük seviyesi, son muma göre daha yüksek
        if prev2_low > curr_high := max(curr_open, curr_close):
            fvg_signals.append((curr_time, 'FVG_UP'))

        # Gap down: önceki 2 mumun en yüksek seviyesi, son muma göre daha düşük
        elif prev2_high < curr_low := min(curr_open, curr_close):
            fvg_signals.append((curr_time, 'FVG_DOWN'))

    return fvg_signals
