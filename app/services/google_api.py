from datetime import datetime

from aiogoogle import Aiogoogle, excs
from app.core.config import settings
from app.services.utils import (
    spreadsheet_body_preset,
    table_header_preset,
    get_rows_count,
    get_columns_count
)
from app.services.constant import FORMAT, ROW_COUNT, COLUMN_COUNT


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = spreadsheet_body_preset(
        now_date_time, ROW_COUNT, COLUMN_COUNT
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return (response['spreadsheetId'], response['spreadsheetUrl'])


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        *table_header_preset(now_date_time),
        *[list(map(
            str,
            [proj['name'], proj['accumulation_time'], proj['description']]
        )) for proj in projects],
    ]
    columns_count = get_columns_count(table_values)
    if columns_count > COLUMN_COUNT:
        raise excs.ValidationError(
            'На вывод пришло больше колонок, чем предусмотрено: '
            f'{columns_count} > {COLUMN_COUNT}'
        )
    rows_count = get_rows_count(table_values)
    if rows_count > ROW_COUNT:
        raise excs.ValidationError(
            'На вывод пришло больше строк, чем предусмотрено: '
            f'{rows_count} > {ROW_COUNT}'
        )
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows_count}C{columns_count}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
