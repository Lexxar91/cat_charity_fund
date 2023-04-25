from sqlalchemy import Column, String, Text

from app.models.base import AbstractCharityAndDonation


class CharityProject(AbstractCharityAndDonation):
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f"<CharityProject(name='{self.name}', invested_amount={self.invested_amount})>"

    
