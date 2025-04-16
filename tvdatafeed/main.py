from tvdatafeed import TvDatafeed, Interval

INTERVAL_MAP = {
    "1m": Interval.min1,
    "5m": Interval.min5,
    "15m": Interval.min15,
    "30m": Interval.min30,
    "1h": Interval.hour1,
    "4h": Interval.hour4,
    "1d": Interval.day1
}

tv = TvDatafeed()

df = tv.get_hist(
    symbol=symbol,
    exchange='BINANCE',
    interval=INTERVAL_MAP[interval],  # doğru eşleşme burada yapılır
    n_bars=300
)
