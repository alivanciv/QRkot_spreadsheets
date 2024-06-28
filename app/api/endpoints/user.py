from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=('auth',),
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=('auth',),
)
users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [
    rout for rout in users_router.routes if rout.name != 'users:delete_user'
]
router.include_router(
    users_router,
    prefix='/users',
    tags=('users',),
)


@router.delete('/{user_id}')
async def remove_user(session: AsyncSession = Depends(get_async_session)):
    """Запрет DELETE запроса к эндпоинту."""
    raise HTTPException(
        status_code=HTTPStatus.METHOD_NOT_ALLOWED,
        detail='Нелья удалять пользователей.'
    )
