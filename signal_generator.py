import logging
from choch_detector import detect_choch
from order_block_detector import detect_order_blocks
from fvg_detector import detect_fvg_zones

def generate_signal(df):
    try:
        choch = detect_choch(df)
        if not choch:
            logging.debug("CHoCH yok, sinyal üretilmedi.")
            return []

        ob = detect_order_blocks(df, choch)
        fvg = detect_fvg_zones(df)

        logging.debug(f"CHOCH: {choch}")
        logging.debug(f"OB:    {ob}")
        logging.debug(f"FVG:   {fvg}")

        final = []
        for ts, direc in choch:
            ob_ok  = any(abs((ts - o[0]).total_seconds()) <= 180 for o in ob)
            fvg_ok = any(abs((ts - f[0]).total_seconds()) <= 180 for f in fvg)
            if ob_ok and fvg_ok:
                sig = "AL" if direc=="CHoCH_UP" else "SAT"
                final.append((ts, sig))
                logging.info(f"→ FINAL SIGNAL @ {ts}: {sig}")

        return final

    except Exception as e:
        logging.error(f"Sinyal üretiminde hata: {e}")
        return []
