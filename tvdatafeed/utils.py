# tvdatafeed/utils.py

import json
import re


class Filter:
    def __init__(self, left, operation, right):
        self.left = left
        self.operation = operation
        self.right = right

    def to_dict(self):
        return {
            "left": self.left,
            "operation": self.operation,
            "right": self.right,
        }


class ScriptFunction:
    def __init__(self, function: str, args: list = None):
        self.function = function
        self.args = args or []

    def to_dict(self):
        return {
            "function": self.function,
            "args": self.args,
        }


def get_symbol(symbol: str, exchange: str):
    return {
        "description": symbol,
        "exchange": exchange,
        "type": "",
    }


def get_interval(interval):
    return {
        "1m": "1",
        "5m": "5",
        "15m": "15",
        "30m": "30",
        "1h": "60",
        "4h": "240",
        "1d": "D",
        "1w": "W",
        "1M": "M",
    }.get(interval, interval)


def convert_to_json(data):
    return json.dumps(data, separators=(",", ":"))


def extract_json(raw):
    pattern = r"\{.*\}"
    matches = re.findall(pattern, raw)
    if matches:
        return json.loads(matches[0])
    raise ValueError("No JSON found")
