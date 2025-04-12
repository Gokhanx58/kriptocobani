# telegram_send.py

from telegram import Bot
import asyncio

# Telegram kanal bilgileri
TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "-1002556449131"

# Son gönderilen sinyalleri tutar
last_signals = {}

# Mesaj gönderme fonksiyonu
async def send_signal_to_channel(symbol, interval, rsi_signal, rmi_signal):
    global last_signals
    key = f"{symbol}_{interval}"
    
    # Yeni sinyalin belirlenmesi
    if rsi_signal == rmi_signal and rsi_signal in ["AL", "SAT"]:
        signal = rsi_signal
    else:
        signal = "BEKLE"
    
    # Önceki sinyalle aynıysa mesaj gönderme
    if last_signals.get(key) == signal:
        return
    last_signals[key] = signal

    # Mesaj içeriği oluşturma
    message = f"📊 {symbol} ({interval}dk): {signal}\n"
    message += f"🔹 RSI Swing: {rsi_signal}\n"
    message += f"🔹 RMI: {rmi_signal}"

    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHANNEL_ID, text=message)
