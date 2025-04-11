from tvDatafeed import TvDatafeed
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
import asyncio

tv = TvDatafeed()

def analyze_signals(symbol, interval, manual=False):
    try:
        exchange = "MEXC"
        interval_map = {
            "1": "1m",
            "5": "5m",
            "15": "15m",
            "30": "30m",
            "60": "1h",
            "4h": "4h",
            "1d": "1d"
        }

        interval_tv = interval_map.get(interval, "1m")
        data = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval_tv, n_bars=100)

        if data is None or data.empty:
            return f"{symbol} ({interval_tv}) için veri alınamadı."

        df = data.copy()
        df.dropna(inplace=True)

        # RMI Trend Sniper (momentum trend)
        rsi = RSIIndicator(close=df["close"], window=14).rsi()
        ema = EMAIndicator(close=df["close"], window=5).ema_indicator()
        mom_positive = (rsi.shift(1) < 60) & (rsi.diff() > 0) & (ema.diff() > 0)
        mom_negative = (rsi.shift(1) > 60) & (rsi.diff() < 0) & (ema.diff() < 0)

        # RSI Swing (HH, LL vs mantıklı basitleştirilmiş)
        swing = "BEKLE"
        if rsi.iloc[-1] > 70 and rsi.iloc[-2] > 70 and df["close"].iloc[-1] < df["close"].iloc[-2]:
            swing = "SAT"
        elif rsi.iloc[-1] < 30 and rsi.iloc[-2] < 30 and df["close"].iloc[-1] > df["close"].iloc[-2]:
            swing = "AL"

        sniper_signal = "AL" if mom_positive.iloc[-1] else "SAT" if mom_negative.iloc[-1] else "BEKLE"

        if swing == sniper_signal and swing != "BEKLE":
            return f"✅ {symbol} ({interval_tv}) için **{swing}** sinyali (her iki indikatör de uyumlu)"
        elif swing != sniper_signal and (swing != "BEKLE" or sniper_signal != "BEKLE"):
            return f"🟡 {symbol} ({interval_tv}) için kararsız sinyal: RSI Swing = {swing}, Trend Sniper = {sniper_signal}"
        else:
            return f"🔘 {symbol} ({interval_tv}) için BEKLE (henüz sinyal yok)"

    except Exception as e:
        return f"{symbol} ({interval}) analiz hatası: {str(e)}"

# Otomatik sinyal fonksiyonu
async def auto_check_signals(bot, chat_id, symbol_list, interval_list, delay):
    while True:
        for symbol in symbol_list:
            for interval in interval_list:
                result = analyze_signals(symbol, interval, manual=False)
                if result and ("AL" in result or "SAT" in result):
                    await bot.send_message(chat_id=chat_id, text=result)
        await asyncio.sleep(delay)
