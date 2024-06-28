from datetime import datetime

from sqlalchemy import select, asc, update
from sqlalchemy.ext.asyncio import AsyncSession


async def get_spread_among_objects(model, session: AsyncSession):
    spread_among_objects = await session.execute(
        select(model)
        .where(model.fully_invested.is_(False))
        # Сортировка по ID для тестов, там у созданых объектов одна дата
        # Сортируя по дате, тесты не проходят, изначально так и делал
        .order_by(asc(model.id))
    )
    return spread_among_objects.scalars().all()


async def update_object(obj, amount: int, session: AsyncSession):
    stmt = (
        update(obj.__class__)
        .where(obj.__class__.id == obj.id)
        .values(invested_amount=obj.__class__.full_amount - amount)
    )
    if amount == 0:
        stmt = (
            update(obj.__class__)
            .where(obj.__class__.id == obj.id)
            .values(
                invested_amount=obj.__class__.full_amount,
                fully_invested=True,
                close_date=datetime.now()
            )
        )
    await session.execute(stmt)


async def process_investments(
        new_db_obj, spread_among_model, session: AsyncSession
):
    spread_among_objects = await get_spread_among_objects(
        spread_among_model, session
    )
    for obj in spread_among_objects:
        if new_db_obj.fully_invested:
            break
        new_db_obj_amount = (
            new_db_obj.full_amount - new_db_obj.invested_amount
        )
        obj_amount = obj.full_amount - obj.invested_amount
        if (new_db_obj_amount > obj_amount):
            amount = obj_amount
        else:
            amount = new_db_obj_amount
        await update_object(
            new_db_obj, new_db_obj_amount - amount, session
        )
        await update_object(
            obj, obj_amount - amount, session
        )
    await session.commit()
    await session.refresh(new_db_obj)
