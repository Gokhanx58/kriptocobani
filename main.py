from bot import application

if __name__ == '__main__':
    application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url="https://kriptocobani.onrender.com"
    )
