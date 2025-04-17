import pandas as pd
import logging

def detect_order_blocks(df: pd.DataFrame, choch_signals):
    order_blocks = []
    for timestamp, direction in choch_signals:
        if timestamp not in df.index:
            continue
        idx = df.index.get_loc(timestamp)
        window = df.iloc[idx+1:idx+4]
        if window.empty:
            continue
        if direction == 'CHoCH_UP':
            for t, candle in window.iterrows():
                if candle['close'] < candle['open']:
                    order_blocks.append((t, 'OB_SHORT', candle['high'], candle['low']))
                    logging.info(f"OB_SHORT @ {t}")
                    break
        else:  # CHoCH_DOWN
            for t, candle in window.iteritems():
                if candle['close'] > candle['open']:
                    order_blocks.append((t, 'OB_LONG', candle['high'], candle['low']))
                    logging.info(f"OB_LONG @ {t}")
                    break
    logging.debug(f"ORDER BLOCKS: {order_blocks}")
    return order_blocks
