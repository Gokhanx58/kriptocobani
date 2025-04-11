import pandas as pd
from ta.momentum import RSIIndicator
from tvDatafeed import TvDatafeed
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'SUIUSDT']
timeframes = ['1m', '5m']

def analyze_signals(symbol, timeframe, manual=False):
    try:
        tv = TvDatafeed()
        df = tv.get_hist(symbol=symbol, exchange='MEXC', interval=timeframe, n_bars=100)

        if df is None or df.empty:
            raise ValueError("Veri alınamadı")

        df['rsi'] = RSIIndicator(df['close'], window=14).rsi()
        df['rsi_signal'] = df['rsi'].apply(lambda x: 'AŞIRI_ALIM' if x > 70 else 'AŞIRI_SATIM' if x < 30 else 'NORM')

        # Dummy RMI simülasyonu (manuel RMI Trend Sniper tanımı için)
        df['rmi_signal'] = df['close'].diff().apply(lambda x: 'AL' if x > 0 else 'SAT')

        rsi = df['rsi_signal'].iloc[-1]
        rmi = df['rmi_signal'].iloc[-1]

        if rsi in ['AŞIRI_ALIM', 'AŞIRI_SATIM'] and rmi == 'AL':
            return f"{symbol} [{timeframe}]: 🔼 AL (RSI: {rsi}, RMI: {rmi})"
        elif rsi in ['AŞIRI_ALIM', 'AŞIRI_SATIM'] and rmi == 'SAT':
            return f"{symbol} [{timeframe}]: 🔽 SAT (RSI: {rsi}, RMI: {rmi})"
        else:
            return f"{symbol} [{timeframe}]: ⏸ BEKLE (RSI: {rsi}, RMI: {rmi})"
    except Exception as e:
        logging.error(f"Veri alınamadı: {e}")
        return f"HATA: {e}"

async def auto_check_signals(bot, chat_id):
    while True:
        try:
            for symbol in symbols:
                for timeframe in timeframes:
                    result = analyze_signals(symbol, timeframe)
                    if "AL" in result or "SAT" in result:
                        await bot.send_message(chat_id=chat_id, text=result)
            await asyncio.sleep(60)
        except Exception as e:
            logging.error(f"Otomatik kontrol hatası: {e}")
            await asyncio.sleep(60)
