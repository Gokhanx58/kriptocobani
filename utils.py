# utils.py

def round_to_nearest(value, precision=0.0001):
    if value is None:
        return "-"
    return round(value, 4)
