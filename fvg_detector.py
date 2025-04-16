import pandas as pd
import logging

def detect_fvg_zones(df: pd.DataFrame, choch_list: list, lookback=5, fvg_threshold=0.2):
    fvg_zones = []

    for choch_time, choch_type in choch_list:
        try:
            choch_idx = df.index.get_loc(choch_time)
        except KeyError:
            continue

        if choch_idx + 3 >= len(df):
            continue

        relevant_df = df.iloc[choch_idx+1:choch_idx+lookback+1]
        if len(relevant_df) < 3:
            continue

        for i in range(2, len(relevant_df)):
            current = relevant_df.iloc[i]
            prev = relevant_df.iloc[i - 2]
            gap_idx = relevant_df.index[i]

            # Bearish FVG: body gap between high[i-2] and low[i]
            if prev['high'] < current['low']:
                gap_size = current['low'] - prev['high']
                if gap_size / prev['high'] >= fvg_threshold:
                    fvg_zones.append((gap_idx, 'FVG_BEARISH', prev['high'], current['low']))
                    break

            # Bullish FVG: body gap between low[i-2] and high[i]
            elif prev['low'] > current['high']:
                gap_size = prev['low'] - current['high']
                if gap_size / prev['low'] >= fvg_threshold:
                    fvg_zones.append((gap_idx, 'FVG_BULLISH', current['high'], prev['low']))
                    break

    logging.warning(f"FVG ZONES: {fvg_zones}")
    return fvg_zones
