from .const import Interval

def get_interval(interval_str: str) -> Interval:
    mapping = {
        "1m": Interval.MIN_1,
        "5m": Interval.MIN_5,
        "15m": Interval.MIN_15,
        "30m": Interval.MIN_30,
        "1h": Interval.HOUR_1,
        "4h": Interval.HOUR_4,
        "1d": Interval.DAY_1,
    }
    return mapping.get(interval_str, Interval.MIN_1)

