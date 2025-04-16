from choch_detector import detect_choch
from order_block_detector import detect_order_blocks
from fvg_detector import detect_fvg
import logging

def generate_signal(df):
    try:
        # CHoCH tespiti
        choch_list = detect_choch(df)
        if not choch_list:
            return None

        last_choch_time, last_choch_dir = choch_list[-1]

        # CHoCH sonrası son 3 barı analiz et
        subset = df[df.index >= last_choch_time]

        if subset.empty:
            return None

        # OB tespiti (bu aralıkta)
        order_blocks = detect_order_blocks(subset)
        if not order_blocks:
            logging.warning("OB bulunamadı")
            return None

        # FVG tespiti (bu aralıkta)
        fvg_zones = detect_fvg(subset)
        if not fvg_zones:
            logging.warning("FVG bulunamadı")
            return None

        # Sinyal üretimi → CHoCH yönüne göre AL/SAT belirle
        if last_choch_dir == 'CHoCH_UP':
            return (last_choch_time, 'AL')
        elif last_choch_dir == 'CHoCH_DOWN':
            return (last_choch_time, 'SAT')
        else:
            return None

    except Exception as e:
        logging.error(f"Sinyal üretiminde hata: {e}")
        return None
