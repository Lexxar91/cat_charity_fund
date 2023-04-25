from app.crud.charity_project import charity_crud
from app.models import CharityProject

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


class ValidatorsClass:
    """
    Класс, содержащий методы-валидаторы для проверки корректности входных данных
    при работе с благотворительными проектами.
    Методы:
    check_charity_project_exists:
        проверяет существование благотворительного проекта с заданным идентификатором.
    check_name_duplicate:
        проверяет отсутствие проекта с заданным именем в базе данных.
    check_invested_amount_in_project:
        проверяет отсутствие вложенных средств в благотворительном проекте.
    count_sum_in_invested_amount:
        проверяет, что устанавливаемая сумма вложений больше или равна уже имеющейся в
    проекте.
    check_charity_project_closed:
        проверяет, что проект еще не закрыт и может быть изменен.
    """
    @staticmethod
    async def check_charity_project_exists(
            charity_project_id: int,
            session: AsyncSession
    ):
        charity_project = await charity_crud.get_object(charity_project_id, session)
        if charity_project is None:
            raise HTTPException(
                status_code=404,
                detail='Благотворительный проект не найден!'
            )
        return charity_project

    @staticmethod
    async def check_name_duplicate(
        charity_name: str,
        session: AsyncSession
    ):
        charity_project_name = await charity_crud.get_charity_id_by_name(charity_name, session)
        if charity_project_name is not None:
            raise HTTPException(
                status_code=400,
                detail='Проект с таким именем уже существует!',
            )
        return None

    @staticmethod
    def check_invested_amount_in_project(charity_project: CharityProject):
        if charity_project.invested_amount > 0:
            raise HTTPException(
                status_code=400,
                detail='В проект были внесены средства, не подлежит удалению!'
            )

    @staticmethod
    def count_sum_in_invested_amount(
            charity_project: CharityProject,
            new_amount: int
    ):
        if charity_project.invested_amount > new_amount:
            raise HTTPException(
                status_code=400,
                detail='Нельзя установить сумму, ниже уже вложенной!'
            )

    @staticmethod
    def check_charity_project_closed(charity_project: CharityProject):
        if charity_project.fully_invested:
            raise HTTPException(
                status_code=400,
                detail='Закрытый проект нельзя редактировать!'
            )
