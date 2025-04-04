from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = os.getenv("TELEGRAM_TOKEN")


def get_klines(symbol="BTCUSDT", interval="1m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol.upper()}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=[
    "timestamp", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
])

    df["close"] = df["close"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["open"] = df["open"].astype(float)
    return df

def calculate_supertrend(df, period=14, multiplier=3):
    atr = ta.volatility.average_true_range(df["high"], df["low"], df["close"], window=period)
    hl2 = (df["high"] + df["low"]) / 2
    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)
    supertrend = [True]
    for i in range(1, len(df)):
        if df["close"][i] > upperband[i - 1]:
            supertrend.append(True)
        elif df["close"][i] < lowerband[i - 1]:
            supertrend.append(False)
        else:
            supertrend.append(supertrend[-1])
    return supertrend

def analyze(symbol="BTCUSDT", interval="1m"):
    df = get_klines(symbol, interval)
    df["rsi"] = ta.momentum.rsi(df["close"], window=14)
    macd = ta.trend.macd(df["close"])
    macd_signal = ta.trend.macd_signal(df["close"])
    df["macd_diff"] = macd - macd_signal
    df["ema20"] = ta.trend.ema_indicator(df["close"], window=20)
    df["ema50"] = ta.trend.ema_indicator(df["close"], window=50)
    df["supertrend"] = calculate_supertrend(df)

    latest = df.iloc[-1]
    comment = []

    rsi = round(latest["rsi"], 2)
    comment.append(f"RSI: {rsi} {'(Aşırı alım)' if rsi > 70 else '(Aşırı satım)' if rsi < 30 else ''}")
    comment.append(f"MACD: {'Al sinyali' if latest['macd_diff'] > 0 else 'Sat sinyali'}")
    comment.append(f"EMA(20/50): {'Pozitif' if latest['ema20'] > latest['ema50'] else 'Negatif'}")
    comment.append(f"Supertrend: {'Long (Al)' if latest['supertrend'] else 'Short (Sat)'}")

    positives = sum([
        latest["rsi"] > 50,
        latest["macd_diff"] > 0,
        latest["ema20"] > latest["ema50"],
        latest["supertrend"]
    ])

    if positives >= 3:
        yorum = "<b>✅ AL</b> Sinyali"
    elif positives <= 1:
        yorum = "<b>❌ SAT</b> Sinyali"
    else:
        yorum = "⚠️ Kararsız"

    return "\n".join(comment) + f"\n\n{yorum}"

def handle_message(update, context):
    text = update.message.text.lower().strip()
    parts = text.split()
    if len(parts) == 2:
        symbol, cmd = parts[0], parts[1]
        symbol = symbol.upper()
        cmd = cmd.lower()

        interval_map = {
            "1": "1m", "5": "5m", "15": "15m", "1h": "1h",
            "4h": "4h", "1d": "1d"
        }

        if cmd == "x":
            intervals = ["1m", "5m", "15m", "1h", "4h", "1d"]
            reply = f"📊 <b>{symbol}</b> Çoklu Zaman Analizi:\n\n"
            for i in intervals:
                try:
                    result = analyze(symbol, i)
                    sinyal = result.splitlines()[-1]
                    reply += f"<b>{i}</b> → {sinyal}\n"
                except:
                    reply += f"<b>{i}</b> → analiz hatası ❌\n"
            update.message.reply_text(reply, parse_mode="HTML")
        elif cmd in interval_map:
            try:
                interval = interval_map[cmd]
                result = analyze(symbol, interval)
                update.message.reply_text(f"📈 <b>{symbol} {interval}</b> Analizi:\n\n{result}", parse_mode="HTML")
            except Exception as e:
                update.message.reply_text(f"Hata: {e}")
        else:
            update.message.reply_text("❌ Geçersiz komut. Örnek: btcusdt 15")
    elif text == "/start":
        update.message.reply_text(
            "📊 Teknik analiz botu aktif!\n\nÖrnek komutlar:\n"
            "`btcusdt 1` → 1 dakikalık analiz\n"
            "`ethusdt 4h` → 4 saatlik analiz\n"
            "`dogeusdt x` → tüm zamanlar",
            parse_mode="HTML"
        )
    else:
        update.message.reply_text("❌ Geçersiz mesaj.")

def run_bot():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", handle_message))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    run_bot()
