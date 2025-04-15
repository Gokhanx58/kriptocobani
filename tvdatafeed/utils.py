# tvdatafeed/utils.py

import json
import random
import string

def get_random_string(length=12):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def tv_json_loads(json_str):
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {}

def create_tv_request_payload(symbol, exchange, interval):
    return {
        "symbol": f"{exchange}:{symbol}",
        "resolution": interval,
        "from": None,  # To be filled with a timestamp
        "to": None,    # To be filled with a timestamp
    }
