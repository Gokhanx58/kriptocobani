import pandas as pd
import logging

def detect_fvg_zones(df: pd.DataFrame):
    """
    Fair Value Gap tespiti yapar ve (timestamp, type, gap_high, gap_low) listesi döner.
    """
    fvg = []
    for i in range(2, len(df)):
        h2 = df['high'].iat[i-2]
        l1 = df['low'].iat[i-1]
        l0 = df['low'].iat[i]
        h1 = df['high'].iat[i-1]

        ts = df.index[i]
        # Boşluk (down gap): önceki low > two bars ago high
        if l1 > h2:
            fvg.append((ts, "FVG_DOWN", l1, h2))
            logging.info(f"FVG_DOWN @ {ts}")

        # Boşluk (up gap): önceki high < current low
        elif h1 < l0:
            fvg.append((ts, "FVG_UP", l0, h1))
            logging.info(f"FVG_UP @ {ts}")

    logging.debug(f"FVG_ZONES: {fvg}")
    return fvg
