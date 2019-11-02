#! /usr/bin/env python3

"""
sakai_stat excel_sheet

reads merged CSV from standard input, compares to provided sakai-exported XLS
"""

import sys
import datetime as dt
try:
    import pandas as pd
except ModuleNotFoundError:
    sys.exit('pandas not found\ninstall with `pip[3] install pandas`')


def main():
    if len(sys.argv) != 2:
        sys.exit(f'usage: {sys.argv[0]} excel_sheet')

    # parse files
    sakai = pd.read_excel(sys.argv[1]).rename(columns={
        'PID': 'pid',
        'Submit time': 'time',
        })[['pid', 'time']]
    checkout = pd.read_csv(sys.stdin).rename(columns={
        'id': 'pid',
        })
    checkout['time'] = pd.to_datetime(checkout['time'])


if __name__ == '__main__':
    main()
