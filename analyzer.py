import logging
from choch_detector import detect_choch
from order_block_detector import detect_order_blocks
from fvg_detector import detect_fvg_zones

def analyze(df):
    choch_list = detect_choch(df)
    order_blocks = detect_order_blocks(df, choch_list)
    fvg_zones = detect_fvg_zones(df, choch_list)

    final_signals = []

    for time, choch_type in choch_list:
        # Aynı timestamp’li OB ve FVG olup olmadığını kontrol et
        ob_matches = [ob for ob in order_blocks if ob[0] == time]
        fvg_matches = [fvg for fvg in fvg_zones if fvg[0] == time]

        if ob_matches and fvg_matches:
            if choch_type == "CHoCH_UP":
                final_signals.append((time, "AL"))
            elif choch_type == "CHoCH_DOWN":
                final_signals.append((time, "SAT"))

    # Loglama (debug için)
    logging.warning(f"CHOCH: {choch_list}")
    logging.warning(f"ORDER BLOCKS: {order_blocks}")
    logging.warning(f"FVG ZONES: {fvg_zones}")
    logging.warning(f"FINAL SIGNALS: {final_signals}")
    logging.warning("====================")

    return final_signals
