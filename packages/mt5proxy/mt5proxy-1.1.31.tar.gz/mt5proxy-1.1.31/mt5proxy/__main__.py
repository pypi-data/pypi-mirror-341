#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: qicongsheng
import argparse
import os
import sys

from . import help
from . import mt5client
from . import proxy

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))


def main():
    parser = argparse.ArgumentParser(f"{help.get_name()} {help.get_version()} ({help.get_source_url()})")
    parser.add_argument('-mt5path', '--mt5path', type=str, help='mt5 installation location', required=False)
    parser.add_argument('-port', '--port', default=8082, type=int, help='http proxy port', required=False)
    parser.add_argument('-users', '--users', type=lambda s: dict(item.split('=') for item in s.split(',')),
                        help='user & passwd')
    args = parser.parse_args()
    mt5client.init(args.mt5path)
    proxy.users = args.users if args.users is not None else proxy.users
    proxy.start(port=args.port)


if __name__ == "__main__":
    main()
