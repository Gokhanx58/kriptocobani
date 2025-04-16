from choch_detector import detect_choch
from order_block_detector import detect_order_blocks
from fvg_detector import detect_fvg
import logging

def generate_signals(df):
    final_signals = []

    # 1. CHoCH, OB ve FVG'leri ayrı ayrı tespit et
    choch_signals = detect_choch(df)
    ob_zones = detect_order_blocks(df, choch_signals)
    fvg_zones = detect_fvg(df)

    # Log kayıtları
    logging.warning("====================")
    logging.warning("CHOCH: %s", choch_signals)
    logging.warning("ORDER BLOCKS: %s", ob_zones)
    logging.warning("FVG ZONES: %s", fvg_zones)

    # Timestamp eşleşmeleriyle sinyal üret
    for choch_time, choch_type in choch_signals:
        matching_ob = [ob for ob in ob_zones if ob[0] == choch_time]
        matching_fvg = [fvg for fvg in fvg_zones if fvg[0] == choch_time]

        if matching_ob and matching_fvg:
            direction = None

            if choch_type == "CHoCH_UP" and matching_ob[0][1] == "OB_LONG" and matching_fvg[0][1] == "FVG_UP":
                direction = "AL"

            elif choch_type == "CHoCH_DOWN" and matching_ob[0][1] == "OB_SHORT" and matching_fvg[0][1] == "FVG_DOWN":
                direction = "SAT"

            if direction:
                final_signals.append((choch_time, direction))

    logging.warning("FINAL SIGNALS: %s", final_signals)
    return final_signals
