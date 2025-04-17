import logging
from choch_detector import detect_choch
from order_block_detector import detect_order_blocks
from fvg_detector import detect_fvg_zones

def analyze(df):
    choch = detect_choch(df)
    if not choch:
        return []

    obs  = detect_order_blocks(df, choch)
    fvgs = detect_fvg_zones(df, choch)

    signals = []
    for ts, direction in choch:
        ob_ok  = any(abs((ts - o[0]).total_seconds()) <= 180 for o in obs)
        fvg_ok = any(abs((ts - f[0]).total_seconds()) <= 180 for f in fvgs)
        if ob_ok and fvg_ok:
            # güçlülük: OB ve FVG çakıştığı mum hacmine veya gap büyüklüğüne bakıp ekleyebilirsiniz.
            strength = ""  # ya da "GÜÇLÜ " mantığı eklenebilir
            sig = f"{strength}AL" if direction=="CHoCH_UP" else f"{strength}SAT"
            signals.append((ts, sig))

    logging.info(f"FINAL SIGNALS: {signals}")
    return signals
