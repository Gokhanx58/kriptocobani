import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# 🔧 Logging ayarı
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# 🔧 Bot token (kendi tokeninle değiştir)
TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"

# ✅ Chat ID yakalama fonksiyonu
async def catch_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logging.info(f"Kanal Chat ID: {chat_id}")
    await update.message.reply_text(
        f"📢 Bu kanalın Chat ID’si: `{chat_id}`", parse_mode="Markdown"
    )

# 🔧 /start komutu (test için)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Kanal chat ID’sini öğrenmek için bu botu kanala yönetici yap ve kanala bir mesaj at.")

# ✅ Ana fonksiyon
async def main():
    app = Application.builder().token(TOKEN).build()

    # Komut ve mesaj yakalayıcılar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, catch_chat_id))  # Tüm mesajları yakala

    # Botu çalıştır
    await app.run_polling()

# ✅ Başlat
if __name__ == "__main__":
    asyncio.run(main())
