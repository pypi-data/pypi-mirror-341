#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: qicongsheng
import os

import MetaTrader5 as mt5
import pandas as pd


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


def get_all_bar_times(symbol, time_frame):
    time_list = []
    current_pos = 0
    chunk_size = 1000  # 每次获取1000根Bar
    while True:
        bars = mt5.copy_rates_from_pos(symbol, time_frame_mapping(time_frame), current_pos, chunk_size)
        if bars is None or len(bars) == 0:
            break
        df = pd.DataFrame(bars)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        time_list.extend(df['time'].tolist())
        current_pos += chunk_size
        # 如果获取的数据少于请求的数量，说明已经到达数据末尾
        if len(bars) < chunk_size:
            break
    return time_list
