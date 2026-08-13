import argparse
import datetime

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

def _count_business_days():
    # 使用例
    start = datetime.date(2025, 7, 10)
    end = datetime.date(2026, 8, 10)
    print(count_business_days(start, end))

if __name__ == '__main__':
    _count_business_days()

#[EOF]
