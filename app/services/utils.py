from datetime import timedelta
import copy

from app.services.constant import BODY, HEADER


def time_format(delta: timedelta):
    days = delta.days
    day_str = 'days'
    if days == 1:
        day_str = 'day'
    time = delta.total_seconds()
    hours: int = time // 3600
    minutes: int = time // 60 % 60
    seconds = time % 60
    return (
        f'{delta.days} {day_str}, '
        f'{hours:.0f}:{minutes:02.0f}:'
        f'{seconds:02.0f}.{delta.microseconds}'
    )


def spreadsheet_body_preset(
        now_date_time: str,
) -> dict:
    body = copy.deepcopy(BODY)
    title = body['properties']['title'].format(now_date_time=now_date_time)
    body['properties']['title'] = title
    return body


def table_header_preset(
        now_date_time: str,
) -> list:
    header = copy.deepcopy(HEADER)
    header[0][1] = header[0][1].format(now_date_time=now_date_time)
    return header


def get_table_size(table_values: list) -> tuple[int, int]:
    rows_count = len(table_values)
    columns_count = max([len(table_values[i]) for i in range(rows_count)])
    return (rows_count, columns_count)
