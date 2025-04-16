from enum import Enum

class Interval(Enum):
    """TradingView veri zaman dilimleri"""
    INTERVAL_1_MINUTE = "1"
    INTERVAL_5_MINUTE = "5"
    INTERVAL_15_MINUTE = "15"
    INTERVAL_30_MINUTE = "30"
    INTERVAL_1_HOUR = "60"
    INTERVAL_4_HOUR = "240"
    INTERVAL_1_DAY = "1D"
    INTERVAL_1_WEEK = "1W"
    INTERVAL_1_MONTH = "1M"
