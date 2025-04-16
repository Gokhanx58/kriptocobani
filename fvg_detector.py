def detect_fvg(df):
    fvg_zones = []

    for i in range(2, len(df)):
        prev_candle = df.iloc[i - 2]
        curr_candle = df.iloc[i]

        # FVG yukarı yönlü: düşük > önceki yüksek
        if curr_candle['low'] > prev_candle['high']:
            fvg_zones.append({
                'timestamp': df.index[i],
                'type': 'FVG_BULLISH',
                'gap_above': prev_candle['high'],
                'gap_below': curr_candle['low']
            })

        # FVG aşağı yönlü: yüksek < önceki düşük
        elif curr_candle['high'] < prev_candle['low']:
            fvg_zones.append({
                'timestamp': df.index[i],
                'type': 'FVG_BEARISH',
                'gap_above': curr_candle['high'],
                'gap_below': prev_candle['low']
            })

    return fvg_zones
