import asyncio
from datetime import datetime, timedelta
from telegram import Bot
from rsi_rmi_analyzer import analyze_signals
from config import TELEGRAM_TOKEN, CHANNEL_ID

bot = Bot(token=TELEGRAM_TOKEN)
sent_signals = {}

async def start_signal_loop():
    symbols = ['BTCUSDT', 'ETHUSDT', 'AVAXUSDT', 'SOLUSDT', 'SUIUSDT']
    intervals = ['1', '5']

    while True:
        for symbol in symbols:
            for interval in intervals:
                result = await analyze_signals(symbol, interval, manual=False)

                if result is None:
                    result = "BEKLE"
                    message = f"{symbol} - {interval}m için analiz sonucu bulunamadı. {result}."
                else:
                    message = f"{symbol} - {interval}m sinyali: {result}"

                key = f"{symbol}_{interval}"
                now = datetime.utcnow()

                # Sinyal değişimi veya 3 dakika kuralı
                if key not in sent_signals:
                    sent_signals[key] = {'signal': result, 'time': now}
                    await bot.send_message(chat_id=CHANNEL_ID, text=message)

                elif result != sent_signals[key]['signal']:
                    sent_signals[key] = {'signal': result, 'time': now}
                    await bot.send_message(chat_id=CHANNEL_ID, text=message)

                elif now - sent_signals[key]['time'] > timedelta(minutes=3):
                    sent_signals[key]['time'] = now
                    await bot.send_message(chat_id=CHANNEL_ID, text=message)

                await asyncio.sleep(10)  # Coinler arası gecikme

        await asyncio.sleep(30)  # Döngü bitince kısa bekleme
