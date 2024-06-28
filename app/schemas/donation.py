from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel, Extra, validator, PositiveInt, Field
)


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid

    @validator('full_amount')
    def full_amount_cannot_be_null(cls, full_amount):
        if full_amount is None:
            raise ValueError('Сумма не может быть NULL!')
        return full_amount


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    create_date: datetime
    user_id: Optional[int] = Field(exclude=True)

    class Config:
        orm_mode = True


class DonationDBAll(DonationDB):
    fully_invested: bool
    close_date: Optional[datetime]
    invested_amount: int
    user_id: int
