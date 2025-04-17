import pandas as pd
import logging

def detect_choch(df: pd.DataFrame):
    choch = []
    swing_high = swing_low = None

    for i in range(3, len(df)):
        prev, curr = df.iloc[i-1], df.iloc[i]
        window = df.iloc[i-3:i]

        # yüksek/düşük belirle
        if prev.high == window.high.max():
            swing_high, sh_time = prev.high, df.index[i-1]
            logging.debug(f"Swing high: {swing_high} @ {sh_time}")
        if prev.low == window.low.min():
            swing_low, sl_time = prev.low, df.index[i-1]
            logging.debug(f"Swing low: {swing_low} @ {sl_time}")

        if swing_high and curr.close > swing_high:
            choch.append((df.index[i], "CHoCH_UP"))
            swing_high = swing_low = None
        elif swing_low and curr.close < swing_low:
            choch.append((df.index[i], "CHoCH_DOWN"))
            swing_high = swing_low = None

    return choch
