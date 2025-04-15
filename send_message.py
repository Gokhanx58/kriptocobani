from telegram import Bot

BOT_TOKEN = "7677308602:AAHH7vloPaQ7PqgFdBnJ2DKYy6sjJ5iqaYE"
CHANNEL_ID = "@GokriptoHan"
bot = Bot(token=BOT_TOKEN)

last_sent_signals = {}

async def send_signal(symbol, interval, new_signal, signal_price, current_price):
    key = f"{symbol}_{interval}"
    last_signal = last_sent_signals.get(key)

    if last_signal == new_signal:
        return  # Sinyal değişmemiş, mesaj gönderme

    # Önceki sinyal varsa ve farklıysa işlem kapat mesajı gönder
    if last_signal and last_signal != new_signal:
        close_msg = f"🔁 *İşlem Kapat Uyarısı*\n🪙 Coin: {symbol}\n⏱️ Zaman: {interval}m\n📌 Önceki Sinyal: {last_signal}\nYeni sinyal geldiği için pozisyon kapatılmalıdır."
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=close_msg, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ İşlem kapatma mesajı hatası: {e}")

    last_sent_signals[key] = new_signal

    emoji = "✅" if "AL" in new_signal else "❌" if "SAT" in new_signal else "⏳"
    yorum = {
        "GÜÇLÜ AL": "Yükseliş beklentisi çok güçlü",
        "AL": "Yükseliş bekleniyor",
        "GÜÇLÜ SAT": "Düşüş baskısı yüksek",
        "SAT": "Geri çekilme bekleniyor",
        "BEKLE": "Sinyal oluşumu bekleniyor"
    }.get(new_signal, "Analiz yapılıyor...")

    mesaj = (
        f"🪙 Coin: {symbol}\n"
        f"⏱️ Zaman: {interval}m\n"
        f"📊 Sistem: CHoCH + Order Block + FVG\n"
        f"📌 Sinyal: {emoji} {new_signal} → {yorum}\n"
        f"💸 Sinyal Fiyatı: {signal_price:.4f}\n"
        f"💰 Şu Anki Fiyat: {current_price:.4f}"
    )

    try:
        print(f"📬 Telegram'a mesaj gönderiliyor: {mesaj}")
        await bot.send_message(chat_id=CHANNEL_ID, text=mesaj)
    except Exception as e:
        print(f"❌ Telegram gönderim hatası: {e}")
