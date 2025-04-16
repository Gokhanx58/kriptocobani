import pandas as pd
import logging

def detect_order_blocks(df: pd.DataFrame, choch_signals):
    """
    CHoCH sonrası oluşan mumlarda Order Block tespiti yapar.
    OB tespiti için CHoCH sinyalinden sonraki 3 muma bakar.

    :param df: OHLCV içeren DataFrame
    :param choch_signals: [(timestamp, direction)] - CHoCH sinyalleri
    :return: [(timestamp, 'OB_LONG' | 'OB_SHORT', high, low)]
    """
    order_blocks = []

    for timestamp, direction in choch_signals:
        if timestamp not in df.index:
            continue

        choch_idx = df.index.get_loc(timestamp)
        lookahead_range = df.iloc[choch_idx+1:choch_idx+4]

        if lookahead_range.empty:
            continue

        if direction == "CHoCH_UP":
            # OB_SHORT: güçlü düşüş mumlarından sonra
            for i in range(len(lookahead_range)):
                candle = lookahead_range.iloc[i]
                if candle['close'] < candle['open']:  # kırmızı mum
                    ob_time = lookahead_range.index[i]
                    high = candle['high']
                    low = candle['low']
                    order_blocks.append((ob_time, "OB_SHORT", high, low))
                    break

        elif direction == "CHoCH_DOWN":
            # OB_LONG: güçlü yeşil mumlardan sonra
            for i in range(len(lookahead_range)):
                candle = lookahead_range.iloc[i]
                if candle['close'] > candle['open']:  # yeşil mum
                    ob_time = lookahead_range.index[i]
                    high = candle['high']
                    low = candle['low']
                    order_blocks.append((ob_time, "OB_LONG", high, low))
                    break

    logging.warning(f"ORDER BLOCKS: {order_blocks}")
    return order_blocks
