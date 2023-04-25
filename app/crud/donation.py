from app.crud.base import CRUDBase
from app.models import User
from app.models.donation import Donation

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class DonationCRUD(CRUDBase):
    """
    DonationCRUD - класс для взаимодействия с моделью Donation в базе данных
    """
    async def get_my_donation(
            self,
            session: AsyncSession,
            user: User
    ):
        my_donation = await session.execute(select(Donation).where(
            Donation.user_id == user.id
        ))
        return my_donation.scalars().all()


donation_crud = DonationCRUD(Donation)
