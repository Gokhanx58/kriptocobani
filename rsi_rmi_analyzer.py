# rsi_rmi_analyzer.py

from utils import get_indicator_data

async def analyze_signals(symbol, interval, manual=False):
    try:
        rsi_sinyal, rmi_sinyal = get_indicator_data(symbol, interval)

        if rsi_sinyal == rmi_sinyal:
            return rsi_sinyal  # AL veya SAT
        elif rsi_sinyal != "BEKLE" or rmi_sinyal != "BEKLE":
            return "BEKLE"
        elif manual:
            return "BEKLE"
        else:
            return None  # Otomatikte aynı sinyal, tekrar etme
    except Exception as e:
        print(f"Analiz hatası ({symbol}-{interval}): {e}")
        return None
