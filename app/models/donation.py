from app.models.base import AbstractCharityAndDonation
from sqlalchemy import Column, ForeignKey, Integer, Text


class Donation(AbstractCharityAndDonation):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
