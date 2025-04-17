import pandas as pd
import logging

def detect_choch(df: pd.DataFrame, window: int = 3):
    """
    CHoCH (Change of Character) tespiti yapar.
    Fiyatın önceki swing high/low seviyelerine göre yön değiştirdiği noktaları bulur.

    :param df: OHLCV içeren DataFrame (timestamp index'li)
    :param window: pivot için bakılacak bar sayısı
    :return: CHoCH sinyalleri listesi: [(timestamp, 'CHoCH_UP' | 'CHoCH_DOWN')]
    """
    choch_signals = []
    swing_high = None
    swing_low = None

    # Index'in sıralı olduğundan emin olalım
    df = df.sort_index()

    for i in range(window, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        # Rolling pivot seviyeleri
        window_high = df['high'].iloc[i - window:i].max()
        window_low  = df['low'].iloc[i - window:i].min()

        # Pivot High
        if prev['high'] == window_high:
            swing_high = prev['high']
            swing_high_time = df.index[i - 1]
            logging.debug(f"Pivot High at {swing_high_time}: {swing_high}")

        # Pivot Low
        if prev['low'] == window_low:
            swing_low = prev['low']
            swing_low_time = df.index[i - 1]
            logging.debug(f"Pivot Low  at {swing_low_time}: {swing_low}")

        # Fiyat kırılımı
        if swing_high is not None and curr['close'] > swing_high:
            logging.info(f"CHoCH_UP at {df.index[i]}: close {curr['close']} > swing_high {swing_high}")
            choch_signals.append((df.index[i], 'CHoCH_UP'))
            swing_high = swing_low = None

        elif swing_low is not None and curr['close'] < swing_low:
            logging.info(f"CHoCH_DOWN at {df.index[i]}: close {curr['close']} < swing_low {swing_low}")
            choch_signals.append((df.index[i], 'CHoCH_DOWN'))
            swing_high = swing_low = None

    logging.warning(f"CHOCH: {choch_signals}")
    return choch_signals
