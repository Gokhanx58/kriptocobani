import pandas as pd
import logging

def detect_order_blocks(df: pd.DataFrame, choch_signals):
    order_blocks = []

    for timestamp, direction in choch_signals:
        if timestamp not in df.index:
            continue
        idx = df.index.get_loc(timestamp)
        lookahead = df.iloc[idx+1:idx+4]
        if lookahead.empty:
            continue

        if direction == "CHoCH_UP":
            # OB_SHORT
            for ts, row in lookahead.iterrows():
                if row['close'] < row['open']:
                    order_blocks.append((ts, "OB_SHORT", row['high'], row['low']))
                    logging.info(f"OB_SHORT @ {ts}")
                    break

        elif direction == "CHoCH_DOWN":
            # OB_LONG
            for ts, row in lookahead.iterrows():
                if row['close'] > row['open']:
                    order_blocks.append((ts, "OB_LONG", row['high'], row['low']))
                    logging.info(f"OB_LONG @ {ts}")
                    break

    logging.debug(f"ORDER_BLOCKS: {order_blocks}")
    return order_blocks
