from sqlalchemy import Column, DateTime, Integer, Boolean
from sqlalchemy.sql import func


class BaseModel:
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, nullable=False, default=func.now())
    close_date = Column(DateTime, default=None)
