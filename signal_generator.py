import logging
from choch_detector import detect_choch
from order_block_detector import detect_order_blocks
from fvg_detector import detect_fvg_zones

def generate_signal(df):
    try:
        choch_list = detect_choch(df)
        if not choch_list:
            logging.warning("CHOCH: []")
            return []

        ob_list  = detect_order_blocks(df, choch_list)
        fvg_list = detect_fvg_zones(df)  # artık tuple listesi

        logging.warning(f"CHOCH: {choch_list}")
        logging.warning(f"ORDER BLOCKS: {ob_list}")
        logging.warning(f"FVG ZONES: {fvg_list}")

        final = []
        for ts, direction in choch_list:
            ob_ok  = any(abs((ts - ob_ts).total_seconds()) <= 180 for ob_ts, *_ in ob_list)
            fvg_ok = any(abs((ts - fvg_ts).total_seconds()) <= 180 for fvg_ts, *_ in fvg_list)
            if ob_ok and fvg_ok:
                sig = 'AL' if direction == 'CHoCH_UP' else 'SAT'
                final.append((ts, sig))

        logging.warning(f"FINAL SIGNALS: {final}")
        return final

    except Exception as e:
        logging.error(f"Sinyal üretiminde hata: {e}")
        return []
