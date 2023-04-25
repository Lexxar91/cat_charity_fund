from typing import Optional

from app.crud.base import CRUDBase
from app.models.charityproject import CharityProject

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDCharityProject(CRUDBase):
    """
    CRUDCharityProject - класс для взаимодействия с моделью CharityProject в базе данных.
    """
    @staticmethod
    async def get_charity_id_by_name(
            charity_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        charity_id = await session.execute(select(CharityProject.id).where(
            CharityProject.name == charity_name
        ))
        charity_id = charity_id.scalars().first()
        return charity_id


charity_crud = CRUDCharityProject(CharityProject)
