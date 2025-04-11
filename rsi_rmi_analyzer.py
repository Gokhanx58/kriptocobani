import time
import logging
import asyncio  # EKLENDİ
from datetime import datetime
from tvDatafeed import TvDatafeed
from ta.momentum import RSIIndicator
import pandas as pd

tv = TvDatafeed()

async def auto_signal_runner(bot, symbol, intervals):
    while True:
        for interval in intervals:
            try:
                msg = analyze_signals(symbol, interval)
                if msg:
                    await bot.send_message(chat_id="@GoKriptoLineBot", text=msg)
                await asyncio.sleep(3)
            except Exception as e:
                logging.error(f"Auto signal error: {e}")
        await asyncio.sleep(60)

def analyze_signals(symbol: str, interval: str, manual=False):
    try:
        df = tv.get_hist(symbol=symbol, exchange='MEXC', interval=interval, n_bars=100)
        if df is None or df.empty:
            raise Exception("Veri alınamadı")

        df['rsi'] = RSIIndicator(close=df['close'], window=14).rsi()
        df['rmi'] = df['rsi'].rolling(window=5).mean()

        rsi_last = df['rsi'].iloc[-1]
        rmi_last = df['rmi'].iloc[-1]

        signal_rsi = ""
        if rsi_last < 30:
            signal_rsi = "RSI: AŞIRI SATIM"
        elif rsi_last > 70:
            signal_rsi = "RSI: AŞIRI ALIM"

        signal_rmi = ""
        if rmi_last > df['rmi'].iloc[-2]:
            signal_rmi = "RMI: YÜKSELİŞ"
        elif rmi_last < df['rmi'].iloc[-2]:
            signal_rmi = "RMI: DÜŞÜŞ"

        final_signal = ""
        if "AŞIRI SATIM" in signal_rsi and "YÜKSELİŞ" in signal_rmi:
            final_signal = "📈 AL"
        elif "AŞIRI ALIM" in signal_rsi and "DÜŞÜŞ" in signal_rmi:
            final_signal = "📉 SAT"
        elif "AŞIRI" in signal_rsi or signal_rmi:
            final_signal = "⏳ BEKLE"

        if manual:
            return f"🔍 {symbol} | {interval} dakikalık analiz:\n\n{signal_rsi}\n{signal_rmi}\n\n📊 Sonuç: {final_signal}"
        else:
            if final_signal in ["📈 AL", "📉 SAT"]:
                return f"🔔 {symbol} | {interval} dakikalık sinyal geldi!\n{signal_rsi}\n{signal_rmi}\n\n➡️ {final_signal}"
            return None

    except Exception as e:
        logging.error(f"Veri alınamadı: {e}")
        return "⚠️ Veri alınamadı."
