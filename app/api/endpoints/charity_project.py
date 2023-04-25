from typing import List

from app.api.validators import ValidatorsClass
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_crud
from app.models import Donation
from app.schemas.charity_project import CharityCreate, CharityDB, CharityUpdate
from app.services.investing import investing_process

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(session: AsyncSession = Depends(get_async_session)) -> List[CharityDB]:
    """
    Получает список всех благотворительных проектов из базы данных.
    Args:
        session (AsyncSession, optional): Сессия базы данных. Defaults to Depends(get_async_session).
    Returns:
        List[CharityDB]: Список объектов благотворительных проектов из базы данных.
    """
    all_charity_projects = await charity_crud.get_all_objects(session)
    return all_charity_projects


@router.post(
    '/',
    response_model=CharityDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
        charity_project: CharityCreate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityDB:
    """
    Создает новый благотворительный проект в базе данных.
    Args:
        charity_project (CharityCreate): Объект создаваемого благотворительного проекта.
        session (AsyncSession, optional): Сессия базы данных. Defaults to Depends(get_async_session).
    Returns:
         CharityDB: Объект созданного благотворительного проекта.
    """
    await ValidatorsClass.check_name_duplicate(charity_project.name, session)
    new_charity = await charity_crud.create(
        charity_project,
        session
    )
    await investing_process(new_charity, Donation, session)
    return new_charity


@router.delete(
    '/{project_id}',
    response_model=CharityDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> CharityDB:
    """
    Удаляет благотворительный проект из базы данных.
    Args:
        project_id (int): Идентификатор удаляемого благотворительного проекта.
        session (AsyncSession, optional): Сессия базы данных. Defaults to Depends(get_async_session).
    Returns:
        CharityDB: Объект удаленного благотворительного проекта.
    """
    delete_charity = await ValidatorsClass.check_charity_project_exists(project_id, session)
    ValidatorsClass.check_invested_amount_in_project(delete_charity)
    delete_charity = await charity_crud.delete(delete_charity, session)
    return delete_charity


@router.patch(
    '/{project_id}',
    response_model=CharityDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
        project_id: int,
        obj_in: CharityUpdate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityDB:
    """
    Обновляет информацию о благотворительном проекте в базе данных.
    Args:
        project_id (int): Идентификатор благотворительного проекта для обновления.
        obj_in (CharityUpdate): Объект с информацией для обновления благотворительного проекта.
        session (AsyncSession, optional): Сессия базы данных. Defaults to Depends(get_async_session).
    Returns:
        CharityDB: Объект обновленного благотворительного проекта.
    """
    charity_project = await ValidatorsClass.check_charity_project_exists(
        project_id, session
    )
    ValidatorsClass.check_charity_project_closed(charity_project)
    if obj_in.name is not None:
        await ValidatorsClass.check_name_duplicate(
            obj_in.name, session
        )
    if obj_in.full_amount is not None:
        ValidatorsClass.count_sum_in_invested_amount(
            charity_project, obj_in.full_amount
        )
    charity_project = await charity_crud.update(
        charity_project, obj_in, session
    )
    return charity_project
