from choch_detector import detect_choch
from order_block_detector import detect_order_blocks
from fvg_detector import detect_fvg
from datetime import timedelta

def analyze(df):
    final_signals = []

    # CHoCH tespiti
    choch_list = detect_choch(df)
    ob_list = detect_order_blocks(df)
    fvg_list = detect_fvg(df)

    for ts, choch_signal in choch_list[-10:]:
        window_start = ts
        window_end = ts + timedelta(minutes=3)

        # OB filtrele
        relevant_obs = [ob for ob in ob_list if window_start <= ob[0] <= window_end]
        # FVG filtrele
        relevant_fvgs = [fvg for fvg in fvg_list if window_start <= fvg[0] <= window_end]

        if relevant_obs and relevant_fvgs:
            final_signals.append((ts, "AL" if choch_signal == "CHoCH_UP" else "SAT"))

    return final_signals
