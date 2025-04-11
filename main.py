import asyncio
from telegram import Bot
from rsi_rmi_analyzer import analyze_signals
import time

# Telegram bot token ve kanal chat_id
TOKEN = '8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs'
CHANNEL_ID = -1002556449131  # @GoKriptoLine kanal ID

bot = Bot(token=TOKEN)

async def send_signal_to_channel(message):
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=message)
        print(f"Mesaj gönderildi: {message}")
    except Exception as e:
        print(f"Hata oluştu: {e}")

async def main():
    while True:
        try:
            for symbol in ["BTCUSDT", "ETHUSDT", "AVAXUSDT", "SUIUSDT", "SOLUSDT"]:
                for interval in ["1m", "5m"]:
                    signal = analyze_signals(symbol, interval)
                    if signal:
                        await send_signal_to_channel(f"{symbol} - {interval} sinyali: {signal}")
                    await asyncio.sleep(3)  # Çakışmaları önle
        except Exception as e:
            print(f"Genel hata: {e}")
        await asyncio.sleep(60)  # 1 dakikada bir çalışır

if __name__ == '__main__':
    asyncio.run(main())
