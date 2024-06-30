FORMAT = '%Y/%m/%d %H:%M:%S'
ROW_COUNT = 100
COLUMN_COUNT = 5

BODY = dict(
    properties=dict(
        title='Отчет от {now_date_time}',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=ROW_COUNT,
            columnCount=COLUMN_COUNT,
        )
    ))]
)

HEADER = [
    ['Отчёт от', '{now_date_time}'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
