def rmi_trend_sniper_signal(df):
    close = df["close"]
    rmi = ta.momentum.RSIIndicator(close=close, window=14).rsi()  # RMI gibi RSI kullanıldı
    ema9 = ta.trend.EMAIndicator(close, window=9).ema_indicator()
    ema21 = ta.trend.EMAIndicator(close, window=21).ema_indicator()
    ema_diff = ema9 - ema21

    positive = (rmi.shift(1) < 66) & (rmi > 66) & (rmi > 30) & (ema_diff > 0)
    negative = (rmi < 30) & (ema_diff < 0)

    if positive.iloc[-1]:
        return "AL"
    elif negative.iloc[-1]:
        return "SAT"
    return "BEKLE"
