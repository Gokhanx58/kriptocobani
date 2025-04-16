from enum import Enum
import pandas as pd

class Interval(Enum):
    in_1_minute = "1m"
    in_5_minute = "5m"

def convert_to_df(data):
    df = pd.DataFrame(data)
    df.set_index('datetime', inplace=True)
    return df
