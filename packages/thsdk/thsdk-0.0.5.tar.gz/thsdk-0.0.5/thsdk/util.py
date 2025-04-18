#!/usr/bin/env python
# -*- coding:utf-8 -*-

__status__ = 'Development'
__author__ = 'xuxiang <xuxiang@nomyhexin.com>'

from .constants import FieldNameMap
from datetime import datetime


def ths_int2time(scr: int) -> datetime:
    m = scr & 63
    h = (scr & 1984) >> 6
    dd = (scr & 63488) >> 11
    mm = (scr & 983040) >> 16
    yyyy = (scr & 133169152) >> 20
    yyyy = 2000 + yyyy % 100

    time_str = f"{yyyy}-{mm:02d}-{dd:02d} {h:02d}:{m:02d}:00"

    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")


def convert_data_keys(data):
    converted_data = []

    for entry in data:
        converted_entry = {}
        for key, value in entry.items():
            if int(key) in FieldNameMap:
                converted_entry[FieldNameMap[int(key)]] = value
            else:
                converted_entry[int(key)] = value
        converted_data.append(converted_entry)

    return converted_data


def market_code2str(market_code: str) -> str:
    if market_code == "17":  # 沪
        return "USHA"
    elif market_code == "22":  # 沪退
        return "USHT"
    elif market_code == "33":  # 深圳退
        return "USZA"
    elif market_code == "37":  # 深圳退
        return "USZP"
    elif market_code == "49":  # 指数
        return "URFI"
    elif market_code == "151":  # 北交所
        return "USTM"
    else:
        raise ValueError("未找到")


def market_str(market_code: str) -> str:
    try:
        return market_code2str(market_code)
    except ValueError:
        return ""
