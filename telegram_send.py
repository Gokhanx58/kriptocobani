# telegram_send.py

import requests

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "@GoKriptoLine"

def send_signal_message(symbol, interval, rsi_sinyal, rmi_sinyal, sonuc):
    emoji_map = {"AL": "🟢", "SAT": "🔴", "BEKLE": "⏸️"}
    mesaj = (
        f"📉 *{symbol}* | ⏱ *{interval}*\n"
        f"🧠 RSI Swing: `{rsi_sinyal}`\n"
        f"🎯 RMI Trend Sniper: `{rmi_sinyal}`\n"
        f"\n{emoji_map.get(sonuc, '')} *Sinyal:* {sonuc}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": mesaj,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, json=payload)
    return response.json()
