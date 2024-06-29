from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import current_superuser, current_user
from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.crud.charity_project import charity_project_crud
from app.crud.base import CRUDBase
from app.models import User
from app.schemas.donation import (
    DonationCreate, DonationDB, DonationDBAll
)
from app.services.investment import process_investments

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Только для юзеров."""
    new_donation = await donation_crud.create(
        donation, session, user, skip_commit=True
    )
    open_projects = await charity_project_crud.get_sorted_open(session)
    process_investments(new_donation, open_projects)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDBAll],
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),),
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Только для юзеров."""
    return await donation_crud.get_by_user(
        session=session, user=user
    )
