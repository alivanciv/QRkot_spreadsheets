from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel, Extra, validator, Field, PositiveInt
)


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid

    @validator('name')
    def name_cannot_be_null(cls, name):
        if name is None:
            raise ValueError('Имя проекта не может быть NULL!')
        return name

    @validator('description')
    def description_cannot_be_null(cls, description):
        if description is None:
            raise ValueError('Описание проекта не может быть NULL!')
        return description

    @validator('full_amount')
    def full_amount_cannot_be_null(cls, full_amount):
        if full_amount is None:
            raise ValueError('Сумма сбора не может быть NULL!')
        return full_amount

    @validator('description')
    def description_not_empty(cls, description: str):
        if not description:
            raise ValueError(
                'Описание проекта не может быть пустым'
            )
        return description


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]


class CharityProjectDB(CharityProjectBase):
    id: int
    fully_invested: bool
    close_date: Optional[datetime]
    invested_amount: int
    create_date: datetime

    class Config:
        orm_mode = True
