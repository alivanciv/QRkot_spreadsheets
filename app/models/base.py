from sqlalchemy import Column, DateTime, Integer, Boolean, CheckConstraint
from sqlalchemy.sql import func


class BaseModel:
    __abstract__ = True
    __table_args__ = (
        CheckConstraint(
            "full_amount > 0",
            name="check_full_amont"
        ),
        CheckConstraint(
            "invested_amount <= full_amount",
            name="check_amounts"
        ),
        CheckConstraint(
            "invested_amount >= 0",
            name="check_invested_amount"
        ),
    )
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, nullable=False, default=func.now())
    close_date = Column(DateTime, default=None)

    def __repr__(self):
        return (
            f'дата создания: {self.create_date}, '
            f'сумма: {self.full_amount}, '
            f'инвестированно: {self.invested_amount}, '
            f'дата закрытия: {self.close_date}' if self.fully_invested else ''
        )
