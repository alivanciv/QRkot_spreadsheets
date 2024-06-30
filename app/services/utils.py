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
        row_count: int,
        column_count: int
) -> dict:
    body = copy.deepcopy(BODY)
    title = body['properties']['title'].format(now_date_time=now_date_time)
    body['properties']['title'] = title
    row = (
        body['sheets'][0]['properties']['gridProperties']['rowCount']
        .format(row_count=row_count)
    )
    body['sheets'][0]['properties']['gridProperties']['rowCount'] = int(row)
    col = (
        body['sheets'][0]['properties']['gridProperties']['columnCount']
        .format(column_count=column_count)
    )
    body['sheets'][0]['properties']['gridProperties']['columnCount'] = int(col)
    return body


def table_header_preset(
        now_date_time: str,
) -> list:
    header = copy.deepcopy(HEADER)
    header[0][1] = header[0][1].format(now_date_time=now_date_time)
    return header


def get_rows_count(table_values: list) -> int:
    return len(table_values)


def get_columns_count(table_values: list) -> int:
    return len(table_values[3])
