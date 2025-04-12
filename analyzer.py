# analyzer.py

from rsi_swing import get_rsi_swing_signal
from rmi_trend_sniper import get_rmi_trend_signal

async def analyze_signals(symbol, interval, manual=False):
    rsi_signal = get_rsi_swing_signal(symbol, interval)
    rmi_signal = get_rmi_trend_signal(symbol, interval)

    if rsi_signal == "AL" and rmi_signal == "AL":
        return f"📈 {symbol} ({interval}dk): AL\n✅ RSI Swing: AL\n✅ RMI: AL"
    elif rsi_signal == "SAT" and rmi_signal == "SAT":
        return f"📉 {symbol} ({interval}dk): SAT\n✅ RSI Swing: SAT\n✅ RMI: SAT"
    elif rsi_signal != rmi_signal:
        return f"⏸️ {symbol} ({interval}dk): BEKLE\n🔁 RSI: {rsi_signal} / RMI: {rmi_signal}"
    else:
        return "⏸️ Sinyal yok"
