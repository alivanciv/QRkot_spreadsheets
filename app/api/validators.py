from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        charity_project_crud_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_crud_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_project_is_open(
        project: int,
        session: AsyncSession,
) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя редактировать закрытые проеткы!'
        )


async def check_invested_amount(
        project: int,
        session: AsyncSession,
) -> None:
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_full_amount(
        project: CharityProject,
        full_amount_in: int,
        session: AsyncSession,
) -> None:
    if full_amount_in < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нелья установить значение full_amount '
                   'меньше уже вложенной суммы.'
        )


async def check_project_to_be_closed(
        project: CharityProject,
        full_amount_in: int,
        session: AsyncSession,
) -> None:
    return full_amount_in < project.invested_amount
