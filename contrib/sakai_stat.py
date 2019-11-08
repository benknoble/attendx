#! /usr/bin/env python3

"""
sakai_stat excel_sheet merged_CSV

reads merged CSV, compares to provided sakai-exported XLS
"""

import sys
import datetime as dt
try:
    import pandas as pd
except ModuleNotFoundError:
    sys.exit('pandas not found\ninstall with `pip[3] install pandas`')


LOCAL_TZ = dt.datetime.now(dt.timezone(dt.timedelta(0))).astimezone().tzinfo
TIME_RANGE_AFTER = 5 * 60  # 5 minutes
TIME_RANGE_BEFORE = 1 * 60  # 1 minutes
TIME_RANGE_UNIT = 's'


def stat(s, co):
    co_uniq = co.drop_duplicates(subset='pid')

    missing_pids = s['pid'][~s['pid'].isin(co_uniq['pid'])]

    co_by_pid = (co
                 .drop_duplicates(subset='pid', keep=False)
                 .set_index('pid')
                 .sort_index())
    s_by_pid = (s
                .set_index('pid')
                .sort_index())
    after_delta_s = ((co_by_pid['time'] - s_by_pid['time'])
                     .dt
                     .total_seconds()
                     .sort_index())
    after = s_by_pid[after_delta_s > TIME_RANGE_AFTER].index
    before_delta_s = ((s_by_pid['time'] - co_by_pid['time'])
                      .dt
                      .total_seconds()
                      .sort_index())
    before = s_by_pid[before_delta_s > TIME_RANGE_BEFORE].index

    def stringify(data):
        return '\n'.join(str(datum) for datum in data)

    return {
            'missing pids': stringify(missing_pids),
            f'left early (submit - checkout > {TIME_RANGE_BEFORE}{TIME_RANGE_UNIT})': stringify(before),
            f'lingered late (checkout - submit > {TIME_RANGE_AFTER}{TIME_RANGE_UNIT})': stringify(after),
           }


def parse(f1, f2):
    sakai = pd.read_excel(f1).rename(columns={
        'PID': 'pid',
        'Submit time': 'time',
        }).dropna(subset=['time'])[['pid', 'time']]
    sakai['time'] = sakai['time'].dt.tz_localize(LOCAL_TZ)

    checkout = pd.read_csv(f2).rename(columns={
        'id': 'pid',
        })
    checkout['time'] = pd.to_datetime(checkout['time']).dt.tz_convert(LOCAL_TZ)

    return (sakai, checkout)


def main():
    if len(sys.argv) != 3:
        sys.exit(f'usage: {sys.argv[0]} excel_sheet merged_csv')

    sakai, checkout = parse(sys.argv[1], sys.argv[2])

    stats = stat(sakai, checkout)
    for name, values in stats.items():
        print(name)
        print('='*len(name))
        print(values)
        print()


if __name__ == '__main__':
    main()
