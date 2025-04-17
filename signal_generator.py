import logging
from choch_detector import detect_choch
from order_block_detector import detect_order_blocks
from fvg_detector import detect_fvg_zones

def generate_signals(df):
    choch = detect_choch(df)
    if not choch:
        return []
    obs = detect_order_blocks(df, choch)
    fvgs = detect_fvg_zones(df)

    logging.debug(f"CHOCH: {choch}")
    logging.debug(f"OBS:   {obs}")
    logging.debug(f"FVG:   {fvgs}")

    results = []
    for ts, dir in choch:
        ok_ob  = any(abs((ts - ob[0]).total_seconds()) <= 180 for ob in obs)
        ok_fvg = any(abs((ts - fvg[0]).total_seconds()) <= 180 for fvg in fvgs)
        if ok_ob and ok_fvg:
            results.append((ts, "AL" if dir=="CHoCH_UP" else "SAT"))

    logging.debug(f"FINAL SIGNALS: {results}")
    return results
