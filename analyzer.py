import pandas as pd
from ta.momentum import RSIIndicator
from tvDatafeed import TvDatafeed

tv = TvDatafeed()

def get_data(symbol, interval, n_bars=100):
    df = tv.get_hist(symbol=symbol, exchange='BINANCE', interval=interval, n_bars=n_bars)
    df = df.dropna()
    df.rename(columns={"close": "Close"}, inplace=True)
    return df

def calculate_rsi_swing(df):
    rsi = RSIIndicator(close=df["Close"], window=7).rsi()
    df["RSI"] = rsi
    df["sinyal"] = ""

    for i in range(1, len(df)):
        if rsi.iloc[i - 1] < 30 and rsi.iloc[i] > 30:
            df.loc[df.index[i], "sinyal"] = "HL"
        elif rsi.iloc[i - 1] > 70 and rsi.iloc[i] < 70:
            df.loc[df.index[i], "sinyal"] = "LH"

    son_sinyal = df["sinyal"].iloc[-1]
    if son_sinyal in ["HL", "LL"]:
        return "AL"
    elif son_sinyal in ["LH", "HH"]:
        return "SAT"
    else:
        return "BEKLE"

def calculate_rmi_trend_sniper(df):
    rsi = RSIIndicator(close=df["Close"], window=14).rsi()
    ema14 = df["Close"].ewm(span=14, adjust=False).mean()
    ema28 = df["Close"].ewm(span=28, adjust=False).mean()
    ema_diff = ema14 - ema28

    positive = (rsi.shift(1) < 66) & (rsi > 66) & (rsi > 30) & (ema_diff > 0)
    negative = (rsi < 30) & (ema_diff < 0)

    if positive.iloc[-1]:
        return "AL"
    elif negative.iloc[-1]:
        return "SAT"
    else:
        return "BEKLE"

async def analyze_signals(symbol: str, interval: str):
    try:
        df = get_data(symbol, interval)
        rsi_result = calculate_rsi_swing(df)
        rmi_result = calculate_rmi_trend_sniper(df)

        if rsi_result == rmi_result:
            final_signal = rsi_result
        elif rsi_result != "BEKLE" or rmi_result != "BEKLE":
            final_signal = "BEKLE"
        else:
            final_signal = None

        return final_signal, rsi_result, rmi_result

    except Exception as e:
        print(f"[analyzer] Hata: {e}")
        return None, "BEKLE", "BEKLE"
