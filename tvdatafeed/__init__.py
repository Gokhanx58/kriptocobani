from .main import TvDatafeed
from .interval import Interval

# tvdatafeed/interval.py
from enum import Enum

class Interval(Enum):
    MIN_1 = '1m'
    MIN_5 = '5m'
    MIN_15 = '15m'
    MIN_30 = '30m'
    HOUR_1 = '1h'
    HOUR_4 = '4h'
    DAY_1 = '1d'
