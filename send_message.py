import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHANNEL

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHANNEL,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=data)
    print(f"Telegram mesaj yanit: {response.status_code} - {response.text}")
    return response.status_code == 200
