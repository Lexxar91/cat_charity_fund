from typing import List

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationCreate, DonationDB, DonationUser
from app.services.investing import investing_process

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True
)
async def get_all_donation(session: AsyncSession = Depends(get_async_session)) -> List[DonationDB]:
    """
    Получение всех пожертвований.
    Args:
        session: Сессия базы данных.
    Returns:
        List[DonationDB]: Список всех пожертвований.
    """
    all_donations = await donation_crud.get_all_objects(session)
    return all_donations


@router.post(
    '/',
    response_model=DonationUser,
    response_model_exclude_none=True
)
async def create_donation(
        donation_create: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> DonationUser:
    """
    Создание нового пожертвования.
    Args:
        donation_create (DonationCreate): Информация о новом пожертвовании.
        session (AsyncSession, optional): Сессия базы данных. По умолчанию `Depends(get_async_session)`.
        user (User, optional): Текущий пользователь. По умолчанию `Depends(current_user)`.
    Returns:
        DonationUser: Информация о пожертвовании и его авторе.
    """
    send_donation = await donation_crud.create(donation_create, session, user)
    await investing_process(send_donation, CharityProject, session)
    return send_donation


@router.get(
    '/my',
    response_model=List[DonationUser],
    response_model_exclude={'user_id'},
)
async def get_my_donation(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> List[DonationUser]:
    """
    Получение всех пожертвований, сделанных текущим пользователем.
    Args:
        session: Сессия базы данных.
        user (User, optional): Текущий пользователь. По умолчанию `Depends(current_user)`.
    Returns:
        List[DonationUser]: Список всех пожертвований, сделанных текущим пользователем.
    """
    donations = await donation_crud.get_my_donation(session, user)
    return donations
