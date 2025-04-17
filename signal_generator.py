import logging
from choch_detector        import detect_choch
from order_block_detector import detect_order_blocks
from fvg_detector         import detect_fvg_zones

def generate_signal(df):
    try:
        choch = detect_choch(df)
        if not choch: return []

        obs = detect_order_blocks(df, choch)
        fvg = detect_fvg_zones(df)

        final = []
        for ts, dir in choch:
            ob_ok  = any(abs((ts - o[0]).total_seconds()) <= 180 for o in obs)
            fvg_ok = any(abs((ts - f[0]).total_seconds()) <= 180 for f in fvg)
            if ob_ok and fvg_ok:
                final.append((ts, 'AL' if dir=='CHoCH_UP' else 'SAT'))

        logging.warning(f"FINAL SIGNALS: {final}")
        return final
    except Exception as e:
        logging.error(f"Sinyal üretiminde hata: {e}")
        return []
