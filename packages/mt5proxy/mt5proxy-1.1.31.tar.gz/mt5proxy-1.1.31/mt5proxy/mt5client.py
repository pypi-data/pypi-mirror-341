#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: qicongsheng
import os
from datetime import datetime, timedelta

import MetaTrader5 as mt5
import pandas as pd
import pytz


def init(path) -> None:
    path = get_backup_mt5path() if path is None or path == '' else path
    if not mt5.initialize(path):
        print("initialize() failed, error code =", mt5.last_error())
        quit()


def get_backup_mt5path() -> str:
    backup_paths = [
        'C:/Program Files/MT5 by FOREX.com Global CN/terminal64.exe',
        'C:/Program Files/mt5/terminal64.exe',
        '/headless/.wine/drive_c/Program\ Files/mt5/terminal64.exe',
    ]
    paths = list(filter(lambda path_: os.path.exists(path_), backup_paths))
    return paths[0] if paths is not None and len(paths) > 0 else None


def time_frame_mapping(time_frame):
    if 'M1' == time_frame:
        return mt5.TIMEFRAME_M1
    if 'M5' == time_frame:
        return mt5.TIMEFRAME_M5
    if 'M15' == time_frame:
        return mt5.TIMEFRAME_M15
    if 'M30' == time_frame:
        return mt5.TIMEFRAME_M30
    if 'H1' == time_frame:
        return mt5.TIMEFRAME_H1
    if 'H4' == time_frame:
        return mt5.TIMEFRAME_H4
    if 'D1' == time_frame:
        return mt5.TIMEFRAME_D1
    if 'W1' == time_frame:
        return mt5.TIMEFRAME_W1
    if 'MN1' == time_frame:
        return mt5.TIMEFRAME_MN1
    return None


def copy_rates_from(symbol, time_frame, date_from, count) -> list:
    return to_ohlcs(symbol, time_frame,
                    mt5.copy_rates_from(symbol, time_frame_mapping(time_frame), date_from, int(count)))


def copy_rates_range(symbol, time_frame, date_from, date_to) -> list:
    return to_ohlcs(symbol, time_frame,
                    mt5.copy_rates_range(symbol, time_frame_mapping(time_frame), date_from, date_to))


def to_ohlcs(symbol: str, time_frame_: str, rates_: list) -> list:
    rates_frame = pd.DataFrame(rates_)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    symbol_info_ = symbol_info(symbol)
    ohlcs = []
    for row in rates_frame.iterrows():
        ohlcs.append({
            'symbol': symbol,
            'time_frame': time_frame_,
            'bar_time': row[1]['time'].strftime("%Y-%m-%d %H:%M:%S"),
            'open': f'%.{symbol_info_.digits}f' % row[1]['open'],
            'high': f'%.{symbol_info_.digits}f' % row[1]['high'],
            'low': f'%.{symbol_info_.digits}f' % row[1]['low'],
            'close': f'%.{symbol_info_.digits}f' % row[1]['close']
        })
    return ohlcs


def symbol_info(symbol):
    return mt5.symbol_info(symbol)


def get_symbols():
    return [{'name': symbol.name, 'digits': symbol.digits} for symbol in mt5.symbols_get()]


def get_all_bars(symbol, time_frame):
    # 首先获取最旧的数据点
    date_from = datetime.strptime('1970060100000', "%Y%m%d%H%M%S").astimezone(pytz.timezone("Etc/UTC"))
    date_to = datetime.strptime('1970120100000', "%Y%m%d%H%M%S").astimezone(pytz.timezone("Etc/UTC"))
    oldest_bars = mt5.copy_rates_range(symbol, time_frame_mapping(time_frame), date_from, date_to)
    if oldest_bars is None or len(oldest_bars) == 0:
        return []
    oldest_time = pd.to_datetime(oldest_bars[0]['time'], unit='s')
    max_bar_time = None
    # 分时间段获取数据(避免一次请求太多数据)
    current_start = oldest_time
    symbol_info_ = symbol_info(symbol)
    ohlcs = []
    while True:
        current_end = current_start + timedelta(days=120)  # 每次获取120天
        bars = mt5.copy_rates_range(symbol, time_frame_mapping(time_frame), current_start, current_end)
        if bars is not None and len(bars) > 0:
            df = pd.DataFrame(bars)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            for row in df.iterrows():
                ohlcs.append({
                    'symbol': symbol,
                    'time_frame': time_frame,
                    'bar_time': row[1]['time'].strftime("%Y-%m-%d %H:%M:%S"),
                    'open': f'%.{symbol_info_.digits}f' % row[1]['open'],
                    'high': f'%.{symbol_info_.digits}f' % row[1]['high'],
                    'low': f'%.{symbol_info_.digits}f' % row[1]['low'],
                    'close': f'%.{symbol_info_.digits}f' % row[1]['close']
                })
            if max_bar_time is not None and max_bar_time == df['time'].iloc[-1]:
                break
            max_bar_time = df['time'].iloc[-1]
            current_start = max_bar_time + timedelta(seconds=1)  # 移动到下一时间段
        else:
            break
    return ohlcs


def get_all_bar_times(symbol, time_frame):
    # 首先获取最旧的数据点
    date_from = datetime.strptime('1970060100000', "%Y%m%d%H%M%S").astimezone(pytz.timezone("Etc/UTC"))
    date_to = datetime.strptime('1970120100000', "%Y%m%d%H%M%S").astimezone(pytz.timezone("Etc/UTC"))
    oldest_bars = mt5.copy_rates_range(symbol, time_frame_mapping(time_frame), date_from, date_to)
    if oldest_bars is None or len(oldest_bars) == 0:
        return []
    oldest_time = pd.to_datetime(oldest_bars[0]['time'], unit='s')
    newest_time = datetime.now()
    # 分时间段获取数据(避免一次请求太多数据)
    time_list = []
    current_start = oldest_time
    while current_start < newest_time:
        current_end = min(current_start + timedelta(days=120), newest_time)  # 每次获取120天
        bars = mt5.copy_rates_range(symbol, time_frame_mapping(time_frame), current_start, current_end)
        if bars is not None and len(bars) > 0:
            df = pd.DataFrame(bars)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            time_list.extend(df['time'].tolist())
            current_start = df['time'].iloc[-1] + timedelta(seconds=1)  # 移动到下一时间段
        else:
            break
    return [time_.strftime('%Y-%m-%d %H:%M:%S') for time_ in sorted(list(set(time_list)))]
