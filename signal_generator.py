import logging
from choch_detector import detect_choch
from order_block_detector import detect_order_blocks
from fvg_detector import detect_fvg_zones

# Ana sinyal üretme fonksiyonu
# CHoCH + OB + FVG uyumunu kontrol eder
def generate_signal(df):
    try:
        choch_list = detect_choch(df)
        ob_list = detect_order_blocks(df)
        fvg_list = detect_fvg_zones(df)

        logging.warning(f"CHOCH: {choch_list}")
        logging.warning(f"ORDER BLOCKS: {ob_list}")
        logging.warning(f"FVG ZONES: {fvg_list}")

        final_signals = []
        for ts, dir in choch_list:
            # OB ve FVG, CHoCH zamanından 3dk içinde olmalı
            ob_ok = any(abs((ts - ob[0]).total_seconds()) <= 180 for ob in ob_list)
            fvg_ok = any(abs((ts - fvg[0]).total_seconds()) <= 180 for fvg in fvg_list)
            if ob_ok and fvg_ok:
                sig = 'AL' if dir == 'CHoCH_UP' else 'SAT'
                final_signals.append((ts, sig))
        logging.warning(f"FINAL SIGNALS: {final_signals}")
        return final_signals
    except Exception as e:
        logging.error(f"Sinyal üretiminde hata: {e}")
        return []
