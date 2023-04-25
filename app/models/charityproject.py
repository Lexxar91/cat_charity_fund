from sqlalchemy import Column, String, Text

from app.models.base import AbstractCharityAndDonation


class CharityProject(AbstractCharityAndDonation):
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
