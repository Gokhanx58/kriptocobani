import pandas as pd

def detect_order_blocks(df, choch_signals):
    df = df.copy()
    order_blocks = []

    for choch_time, choch_type in choch_signals:
        idx = df.index.get_loc(choch_time)

        # CHoCH sonrası gelen 1-2 mum analiz edilecek
        for offset in range(1, 3):
            if idx + offset >= len(df):
                continue

            row = df.iloc[idx + offset]
            body_size = abs(row['close'] - row['open'])
            candle_range = row['high'] - row['low']

            # Güçlü bir gövde varsa OB olarak değerlendir
            if body_size >= 0.6 * candle_range:
                if choch_type == 'CHoCH_UP' and row['close'] < row['open']:
                    order_blocks.append((df.index[idx + offset], "OB_SHORT", row['high'], row['low']))
                    break
                elif choch_type == 'CHoCH_DOWN' and row['close'] > row['open']:
                    order_blocks.append((df.index[idx + offset], "OB_LONG", row['high'], row['low']))
                    break

    return order_blocks
