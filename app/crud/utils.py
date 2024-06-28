from datetime import timedelta


def time_format(delta: timedelta):
    days = delta.days
    day_str = 'days'
    if days == 1:
        day_str = 'day'
    time = delta.total_seconds()
    hours: int = time // 3600
    minutes: int = time // 60 % 60
    seconds = time % 60
    return (f'{delta.days} {day_str}, '
            f'{hours:.0f}:{minutes:02.0f}:'
            f'{seconds:02.0f}.{delta.microseconds}')
