# telegram_send.py

import requests

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "@GoKriptoLine"

def send_telegram_message(symbol: str, interval: str, final_signal: str, rsi_swing_signal: str, rmi_signal: str):
    signal_emoji = {
        "AL": "✅",
        "SAT": "🚫",
        "BEKLE": "⏳"
    }

    direction_emoji = {
        "AL": "📈",
        "SAT": "📉",
        "BEKLE": "〰️"
    }

    message = (
        f"{direction_emoji.get(final_signal, '')} <b>{symbol}</b> ({interval}): <b>{final_signal}</b>\n"
        f"{signal_emoji.get(rsi_swing_signal, '')} <b>RSI Swing:</b> {rsi_swing_signal}\n"
        f"{signal_emoji.get(rmi_signal, '')} <b>RMI:</b> {rmi_signal}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    print(f"[Telegram] Status Code: {response.status_code}, Response: {response.text}")
