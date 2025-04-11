from datetime import datetime, timedelta
from utils import get_indicator_data

# Son gönderilen sinyalleri takip etmek için hafızada tutulan değişken
last_sent_signals = {}

async def analyze_signals(symbol, interval, manual=False):
    try:
        # RSI Swing ve RMI Trend Sniper analizini çekiyoruz
        rsi_swing_signal, rmi_sniper_signal = get_indicator_data(symbol, interval)

        # İkisi de aynı yönde sinyal veriyorsa
        if rsi_swing_signal == rmi_sniper_signal and rsi_swing_signal in ["AL", "SAT"]:
            final_signal = rsi_swing_signal
        # Sadece biri sinyal veriyorsa, diğerinin beklemede olduğunu bildir
        elif rsi_swing_signal in ["AL", "SAT"] or rmi_sniper_signal in ["AL", "SAT"]:
            final_signal = f"BEKLE ({'RSI: ' + rsi_swing_signal if rsi_swing_signal != 'BEKLE' else ''}{' | ' if rsi_swing_signal != 'BEKLE' and rmi_sniper_signal != 'BEKLE' else ''}{'RMI: ' + rmi_sniper_signal if rmi_sniper_signal != 'BEKLE' else ''})"
        # Hiçbiri sinyal vermiyorsa
        else:
            final_signal = "BEKLE"

        # Eğer komutla çağrıldıysa sonucu direkt döndür
        if manual:
            return final_signal

        # Aşağıdan itibaren sadece otomatik çalışan botlar için geçerli
        key = f"{symbol}_{interval}"
        now = datetime.utcnow()
        last = last_sent_signals.get(key)

        # Sadece sinyal değişmişse VEYA son gönderim 3 dakikayı geçmişse gönderim yap
        if not last or last["signal"] != final_signal or (now - last["time"]) > timedelta(minutes=3):
            last_sent_signals[key] = {"signal": final_signal, "time": now}
            return final_signal
        else:
            return None

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None
