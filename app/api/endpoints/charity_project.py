from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import current_superuser
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.api.validators import (
    check_name_duplicate, check_charity_project_exists,
    check_invested_amount, check_project_is_open,
    check_full_amount, check_project_to_be_closed
)
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.crud.investment import process_investments
from app.models.donation import Donation

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),),
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    await process_investments(new_project, Donation, session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),),
)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    await check_project_is_open(charity_project, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_full_amount(
            charity_project,
            obj_in.full_amount,
            session
        )
        if await check_project_to_be_closed(
            charity_project, obj_in.full_amount, session
        ):
            await charity_project_crud.close_project(charity_project, session)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),),
)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    await check_invested_amount(charity_project, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
