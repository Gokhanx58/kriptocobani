import logging
from choch_detector import detect_choch
from order_block_detector import detect_order_blocks
from fvg_detector import detect_fvg_zones

def generate_signal(df):
    try:
        choch_list = detect_choch(df)
        if not choch_list:
            logging.debug("CHoCH yok, sinyal üretilmedi.")
            return []
        ob_list = detect_order_blocks(df, choch_list)
        fvg_list = detect_fvg_zones(df)
        logging.debug(f"CHOCH: {choch_list}")
        logging.debug(f"ORDER BLOCKS: {ob_list}")
        logging.debug(f"FVG ZONES: {fvg_list}")

        final_signals = []
        for ts, direc in choch_list:
            ob_ok = any(abs((ts - ob[0]).total_seconds()) <= 180 for ob in ob_list)
            fvg_ok = any(abs((ts - fvg[0]).total_seconds()) <= 180 for fvg in fvg_list)
            if ob_ok and fvg_ok:
                sig = 'AL' if direc == 'CHoCH_UP' else 'SAT'
                final_signals.append((ts, sig))
                logging.info(f"FINAL_SIGNAL: {sig} @ {ts}")
        logging.debug(f"FINAL SIGNALS: {final_signals}")
        return final_signals
    except Exception as e:
        logging.error(f"Sinyal üretim hatası: {e}")
        return []
