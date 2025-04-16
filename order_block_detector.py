import pandas as pd

def detect_order_blocks(df: pd.DataFrame, choch_signals):
    order_blocks = []
    df = df.copy()
    df['body'] = abs(df['close'] - df['open'])

    for timestamp, choch_type in choch_signals:
        choch_index = df.index.get_loc(timestamp)
        lookahead = df.iloc[choch_index + 1: choch_index + 4]

        if choch_type == 'CHoCH_DOWN':
            candidate = lookahead[lookahead['close'] > lookahead['open']]
            if not candidate.empty:
                order_blocks.append((timestamp, 'OB_LONG', candidate['high'].iloc[0], candidate['low'].iloc[0]))

        elif choch_type == 'CHoCH_UP':
            candidate = lookahead[lookahead['close'] < lookahead['open']]
            if not candidate.empty:
                order_blocks.append((timestamp, 'OB_SHORT', candidate['high'].iloc[0], candidate['low'].iloc[0]))
    return order_blocks
