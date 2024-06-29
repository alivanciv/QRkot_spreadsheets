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
    return dict(
        properties=dict(
            title=f'Отчет от {now_date_time}',
            locale='ru_RU',
        ),
        sheets=[dict(properties=dict(
            sheetType='GRID',
            sheetId=0,
            title='Лист1',
            gridProperties=dict(
                rowCount=row_count,
                columnCount=column_count,
            )
        ))]
    )


def table_header_preset(
        now_date_time: str,
) -> list:
    return [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
