from choch_detector import detect_choch
from order_block_detector import detect_order_blocks
from fvg_detector import detect_fvg
import logging
from datetime import timedelta

def generate_signals(df):
    final_signals = []
    choch_signals = detect_choch(df)
    ob_zones = detect_order_blocks(df, choch_signals)
    fvg_zones = detect_fvg(df)

    logging.warning("====================")
    logging.warning("CHOCH: %s", choch_signals)
    logging.warning("ORDER BLOCKS: %s", ob_zones)
    logging.warning("FVG ZONES: %s", fvg_zones)

    for choch_time, choch_type in choch_signals:
        # Zaman toleransı 60 saniye (1 dakika)
        ob_match = next((ob for ob in ob_zones if abs((ob[0] - choch_time).total_seconds()) <= 60), None)
        fvg_match = next((fvg for fvg in fvg_zones if abs((fvg[0] - choch_time).total_seconds()) <= 60), None)

        if ob_match and fvg_match:
            if choch_type == "CHoCH_UP" and ob_match[1] == "OB_LONG" and fvg_match[1] == "FVG_UP":
                final_signals.append((choch_time, "AL"))
            elif choch_type == "CHoCH_DOWN" and ob_match[1] == "OB_SHORT" and fvg_match[1] == "FVG_DOWN":
                final_signals.append((choch_time, "SAT"))

    logging.warning("FINAL SIGNALS: %s", final_signals)
    return final_signals
