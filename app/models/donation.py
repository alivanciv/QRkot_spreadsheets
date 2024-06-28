from sqlalchemy import Column, Integer, Text, ForeignKey

from app.core.db import Base
from app.models.base import BaseModel


class Donation(Base, BaseModel):
    comment = Column(Text)
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user')
    )
