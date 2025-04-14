# telegram_send.py (güncel, optimize edilmiş ve özelleştirilmiş mesaj yapısı)

from telegram import Bot

BOT_TOKEN = "8002562873:AAHoMdOpiZEi2XILMmrwAOjtyKEWNMVLKcs"
CHANNEL_ID = "@GoKriptoLine"
bot = Bot(token=BOT_TOKEN)

# Sinyal geçmişini takip etmek için sözlük
last_signals = {}

async def send_signal_to_channel(symbol, interval, signal, price):
    key = f"{symbol}_{interval}"
    onceki_sinyal = last_signals.get(key)

    # Aynı sinyal tekrar edilmesin
    if onceki_sinyal == signal:
        return

    emoji = "✅" if signal == "AL" else "❌" if signal == "SAT" else "⏳"
    detay = "Yükseliş bekleniyor" if signal == "AL" else "Geri çekilme bekleniyor" if signal == "SAT" else "Sinyal bekleniyor"

    # Sistem gücü yorumu
    sistem_durum = "Güçlü AL" if signal == "AL" and "strong" in signal.lower() else \
                    "Güçlü SAT" if signal == "SAT" and "strong" in signal.lower() else \
                    signal  # AL veya SAT

    cikis_mesaji = f"🔁 Pozisyon değişimi!\n⛔ {onceki_sinyal} pozisyonundan çıkılıyor.\n\n" if onceki_sinyal in ["AL", "SAT"] else ""

    mesaj = (
        f"{cikis_mesaji}"
        f"🪙 {symbol} | ⏱️ {interval}m\n"
        f"💰 Sinyal Fiyatı: {price:.2f} USDT\n"
        f"📊 Sistem Durumu: {sistem_durum}\n"
        f"📌 Sinyal: {emoji} {signal} → {detay}"
    )

    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=mesaj)
        last_signals[key] = signal  # Yeni sinyali kaydet
    except Exception as e:
        print(f"Telegram gönderim hatası: {e}")
