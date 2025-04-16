import pandas as pd
import logging
from choch_detector import detect_choch
from order_block_detector import detect_order_blocks
from fvg_detector import detect_fvg

logger = logging.getLogger(__name__)


def generate_signals(df):
    choch_signals = detect_choch(df)
    order_blocks = detect_order_blocks(df)
    fvg_zones = detect_fvg(df)

    logger.warning(f"CHOCH: {choch_signals}")
    logger.warning(f"ORDER BLOCKS: {order_blocks}")
    logger.warning(f"FVG ZONES: {fvg_zones}")

    final_signals = []

    for choch_time, choch_type in choch_signals:
        choch_index = df.index.get_loc(choch_time)
        future_range = df.iloc[choch_index + 1:choch_index + 6]  # 5 bar ileriye bak

        ob_match = None
        fvg_match = None

        for ob_time, ob_type, *_ in order_blocks:
            if choch_time < ob_time <= choch_time + pd.Timedelta(minutes=3):
                if (choch_type == 'CHoCH_UP' and ob_type == 'OB_LONG') or \
                   (choch_type == 'CHoCH_DOWN' and ob_type == 'OB_SHORT'):
                    ob_match = (ob_time, ob_type)
                    break

        for fvg_time, fvg_type in fvg_zones:
            if choch_time < fvg_time <= choch_time + pd.Timedelta(minutes=3):
                if (choch_type == 'CHoCH_UP' and fvg_type == 'FVG_UP') or \
                   (choch_type == 'CHoCH_DOWN' and fvg_type == 'FVG_DOWN'):
                    fvg_match = (fvg_time, fvg_type)
                    break

        if ob_match and fvg_match:
            signal_type = 'AL' if choch_type == 'CHoCH_UP' else 'SAT'
            final_signals.append((choch_time, signal_type))

    logger.warning(f"FINAL SIGNALS: {final_signals}")
    logger.warning("====================")

    return final_signals
