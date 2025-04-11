import asyncio
import logging
from telegram.ext import Application, CommandHandler
from rsi_rmi_analyzer import analyze_signals, auto_signal_runner

logging.basicConfig(level=logging.INFO)

TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"

async def handle_analysis(update, context):
    if len(context.args) != 2:
        await update.message.reply_text("Kullanım: /analiz COIN ZAMAN (örn: /analiz BTCUSDT 5)")
        return

    symbol = context.args[0].upper()
    interval = context.args[1]

    result = analyze_signals(symbol, interval, manual=True)
    await update.message.reply_text(result)

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("analiz", handle_analysis))

    asyncio.create_task(auto_signal_runner())  # Otomatik sinyal üretimi
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
