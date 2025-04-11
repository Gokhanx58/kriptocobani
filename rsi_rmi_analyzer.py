import logging
import asyncio
from tvDatafeed import TvDatafeed, Interval
from telegram import Bot

logging.basicConfig(level=logging.INFO)

bot = Bot(token="8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs")
chat_id = "@GoKriptoLineBot"

tv = TvDatafeed()  # nologin

symbol_list = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "SUIUSDT"]
interval_mapping = {"1": Interval.in_1_minute, "5": Interval.in_5_minute}

def analyze_signals(symbol, interval, manual=False):
    try:
        tv_interval = interval_mapping.get(str(interval))
        if not tv_interval:
            return "Geçersiz zaman dilimi. Sadece 1 veya 5 dakika destekleniyor."

        data = tv.get_hist(symbol=symbol, exchange='MEXC', interval=tv_interval, n_bars=100)
        if data is None or data.empty:
            return "Veri alınamadı."

        close = data["close"]
        if isinstance(close.iloc[-1], str):
            return "Veri alınamadı: 'str' object has no attribute 'value'"

        son_kapanis = close.iloc[-1]
        onceki_kapanis = close.iloc[-2]

        rmi_signal = "AL" if son_kapanis > onceki_kapanis else "SAT"
        rsi_signal = "AL" if son_kapanis > close.mean() else "SAT"

        if rmi_signal == rsi_signal:
            mesaj = f"{symbol} ({interval}dk) ➤ {rmi_signal}"
        else:
            mesaj = f"{symbol} ({interval}dk) ➤ BEKLE (RMI: {rmi_signal}, RSI: {rsi_signal})"

        return mesaj

    except Exception as e:
        logging.error(f"Veri alınamadı: {e}")
        return "Veri alınamadı"

async def auto_signal_runner():
    while True:
        try:
            for symbol in symbol_list:
                for interval in ["1", "5"]:
                    result = analyze_signals(symbol, interval)
                    if "➤ AL" in result or "➤ SAT" in result:
                        try:
                            await bot.send_message(chat_id=chat_id, text=result)
                        except Exception as e:
                            logging.error(f"Auto signal error: {e}")
                    await asyncio.sleep(3)  # Her sorgu arası bekleme
            await asyncio.sleep(60)  # Tüm döngü sonrası 1 dakika bekleme
        except Exception as e:
            logging.error(f"Auto signal error: {e}")
            await asyncio.sleep(10)
