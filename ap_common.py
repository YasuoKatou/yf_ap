import argparse
import datetime
import os

import jpholiday

def getArgs(params):
    parser = argparse.ArgumentParser()
    for name, value in params.items():
        _help = value['help'] if 'help' in value else None
        _type = value['type'] if 'type' in value else None
        _default = value['default'] if 'default' in value else None
        parser.add_argument(name, help=_help, default=_default, type=_type)
    return parser.parse_args()

def count_business_days(start_date, end_date):
    current = start_date
    business_days = 0
    while current <= end_date:
        # 土日（5, 6）でも祝日でもなければカウント
        if current.weekday() < 5 and not jpholiday.is_holiday(current):
            business_days += 1
        current += datetime.timedelta(days=1)
    return business_days

def sub_business_days(start_date, day_count):
    current = start_date
    while 0 < day_count:
        current -= datetime.timedelta(days=1)
        # 土日（5, 6）でも祝日でもなければカウント
        if current.weekday() < 5 and not jpholiday.is_holiday(current):
            day_count -= 1
    return current

def _count_business_days():
    # 使用例
    start = datetime.date(2025, 7, 10)
    end = datetime.date(2026, 8, 10)
    print(count_business_days(start, end))

def _sub_business_days():
    start = datetime.date(2026, 8, 19)
    sub_days = 2
    print(f'base date {start} - {sub_days}days = {sub_business_days(start, sub_days)}')
    sub_days = 3
    print(f'base date {start} - {sub_days}days = {sub_business_days(start, sub_days)}')
    sub_days = 4
    print(f'base date {start} - {sub_days}days = {sub_business_days(start, sub_days)}')

def get_env_dbwork():
    return os.getenv('sqlite_work')

if __name__ == '__main__':
    #_count_business_days()
    #_sub_business_days()
    print(f'sqlite_work : {get_env_dbwork()}')

#[EOF]
