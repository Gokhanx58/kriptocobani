from choch_detector import detect_choch
from order_block_detector import detect_order_blocks
from fvg_detector import detect_fvg
import pandas as pd

def generate_signals(df: pd.DataFrame):
    choch_signals = detect_choch(df)
    ob_zones = detect_order_blocks(df, choch_signals)
    fvg_zones = detect_fvg(df)
    signals = []

    for ts, choch_type in choch_signals:
        matching_ob = next((ob for ob in ob_zones if ob[0] == ts), None)
        if not matching_ob:
            continue

        _, ob_type, _, _ = matching_ob
        matching_fvg = [fvg for fvg in fvg_zones if abs((fvg[0] - ts).total_seconds()) < 180]
        if not matching_fvg:
            continue

        fvg_type = matching_fvg[0][1]

        if choch_type == 'CHoCH_DOWN' and ob_type == 'OB_LONG' and fvg_type == 'FVG_DOWN':
            signals.append((ts, 'AL'))
        elif choch_type == 'CHoCH_UP' and ob_type == 'OB_SHORT' and fvg_type == 'FVG_UP':
            signals.append((ts, 'SAT'))

    return signals
