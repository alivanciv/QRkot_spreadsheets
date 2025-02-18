from datetime import datetime

from app.models import BaseModel


def process_investments(
        target: BaseModel,
        sources: list[BaseModel]
) -> list[BaseModel]:
    updated_sources = []
    for source in sources:
        if target.fully_invested:
            break
        amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for object in [target, source]:
            object.invested_amount += amount
            if object.invested_amount == object.full_amount:
                object.fully_invested = True
                object.close_date = datetime.now()
        updated_sources.append(source)
    return updated_sources
