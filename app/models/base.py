from datetime import datetime

from app.core.db import Base
from sqlalchemy import Boolean, Column, DateTime, Integer


class AbstractCharityAndDonation(Base):
    """
    AbstractCharityAndDonation - абстрактный базовый класс, определяющий общую структуру для моделей CharityProject и
    Donation.
    """
    __abstract__ = True
    full_amount = Column(Integer, nullable=False, default=0)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    close_date = Column(DateTime)
