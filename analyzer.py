import logging
from choch_detector import detect_choch
from order_block_detector import detect_order_blocks
from fvg_detector import detect_fvg_zones

def analyze(df):
    choch = detect_choch(df)
    ob = detect_order_blocks(df, choch)
    fvg = detect_fvg_zones(df)

    final = []
    for ts, d in choch:
        if any(o[0]==ts for o in ob) and any(f[0]==ts for f in fvg):
            final.append((ts, "AL" if d=="CHoCH_UP" else "SAT"))

    logging.debug(f"CHOCH: {choch}")
    logging.debug(f"OB:    {ob}")
    logging.debug(f"FVG:   {fvg}")
    logging.info(f"FINAL: {final}\n{'='*20}")
    return final
