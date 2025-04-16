# tvdatafeed/interval.py
from enum import Enum

class Interval(Enum):
    min1 = "1"
    min5 = "5"
    min15 = "15"
    min30 = "30"
    hour1 = "60"
    hour4 = "240"
    day1 = "D"
