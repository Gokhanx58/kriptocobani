# tvdatafeed/utils.py

import json
import re


def generate_session(prefix="qs"):
    return prefix + "_" + "".join(re.sample("abcdefghijklmnopqrstuvwxyz0123456789", 12))


def construct_message(func, param):
    return json.dumps({"m": func, "p": param}, separators=(',', ':'))


def create_message(func, param):
    message = construct_message(func, param)
    return f'{len(message)}\n{message}'
