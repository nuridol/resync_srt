#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# encoding=utf8

import argparse
import io
import logging
import logging.handlers
import os
import re
import sys

# settings
APP_VERSION = '1.0'

# log
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def convert_ms(time_str):
    m = re.match(r'(\d+):(\d+):(\d+),(\d+)', time_str)
    ms = int(m.group(1))*60*60*1000 + int(m.group(2))*60*1000 + int(m.group(3))*1000 + int(int(m.group(4))/1000*1000)
    return ms


def convert_timestamp(ms):
    str_ms = ms % 1000
    base_sec = int(ms / 1000)
    hour = int(base_sec / 3600)
    base_sec = base_sec - 3600*hour
    minute = int(base_sec / 60)
    sec = base_sec - 60*minute
    return f'{hour:02}:{minute:02}:{sec:02},{str_ms:03}'


def resync(file_path, offset=0, rate=1.0):
    logger.debug(file_path)
    if not os.path.exists(file_path):
        logger.error(f'{file_path} not found!')
        return
    filename, file_extension = os.path.splitext(file_path)
    if '.srt' != file_extension.lower():
        logger.error(f'{file_path} is not SRT!')
        return

    new_file_path = f'{filename}.resync{file_extension}'
    logger.info(f'Start resync - rate: x{rate} / offset: {offset}ms')
    logger.info(f'Source: {file_path} / Output: {new_file_path}')
    try:
        with open(file_path, encoding='UTF-8') as f:
            with open(new_file_path, encoding='UTF-8', mode='w') as new_file:
                time_pattern = re.compile(r'(\d+:\d+:\d+,\d+) +--> +(\d+:\d+:\d+,\d+)')
                for line in f:
                    if time_pattern.fullmatch(line.strip()):
                        # 00:00:04,120 --> 00:00:08,690
                        m = re.match(time_pattern, line)
                        start_time_ms = convert_ms(m.group(1))
                        end_time_ms = convert_ms(m.group(2))
                        new_start_time_ms = int(start_time_ms * rate + offset)
                        new_end_time_ms = int(end_time_ms * rate + offset)
                        new_timeline = f'{convert_timestamp(new_start_time_ms)} --> {convert_timestamp(new_end_time_ms)}'
                        logger.debug(f'Change timeline [{line.strip()}] to [{new_timeline}]')
                        new_file.write(new_timeline + '\n')
                    else:
                        new_file.write(line)
        logger.info(f'done!')

    except Exception as e:
        logger.error(e, exc_info=True)

    return


def init():
    if sys.platform == 'win32' and sys.stdout.encoding != 'cp65001':
        os.system("echo off")
        os.system("chcp 65001")  # Change active page code

    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    # stdout
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)
    c_format = logging.Formatter('%(asctime)s - %(message)s')
    c_handler.setFormatter(c_format)
    logger.addHandler(c_handler)
    logger.propagate = False
    return

def main():
    # ready
    app_name = f'RE:Sync SRT v{APP_VERSION}'
    parser = argparse.ArgumentParser(description=app_name)
    parser.add_argument('file', type=str, help='SRT file')
    parser.add_argument('--debug', action='store_true', help='print debug message')
    parser.add_argument('--offset', type=int, default=0, help='sync offset(ms)')
    parser.add_argument('--rate', type=float, default=1.0, help='sync rate')

    args = parser.parse_args()

    # debug mode
    if args.debug:
        logger.setLevel(logging.DEBUG)

    # init
    init()

    # resync
    resync(args.file, args.offset, args.rate)

    return


# ===============
# MAIN
# ===============
if __name__ == "__main__":
    main()
