def rsi_swing_signal(df, rsi_period=7):
    df["rsi"] = ta.momentum.RSIIndicator(close=df["close"], window=rsi_period).rsi()
    df["sinyal"] = None

    for i in range(2, len(df)):
        prev = df.iloc[i - 1]["rsi"]
        curr = df.iloc[i]["rsi"]

        # HL, LL, HH, LH mantığı
        if prev < 30 and curr > prev and curr < 70:
            label = "HL"
        elif prev > 70 and curr < prev and curr > 30:
            label = "LH"
        elif prev < 30 and curr > 30:
            label = "LL"
        elif prev > 70 and curr < 70:
            label = "HH"
        else:
            label = None

        if label:
            df["sinyal"].iloc[i] = label

    # Sinyal karar mantığı
    last_label = df["sinyal"].dropna().iloc[-1] if not df["sinyal"].dropna().empty else None
    if last_label in ["HL", "LL"]:
        return "AL"
    elif last_label in ["HH", "LH"]:
        return "SAT"
    return "BEKLE"
