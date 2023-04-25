from typing import Optional

from app.models import User

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    """
    Базовый класс для выполнения операций CRUD (Create, Read, Update, Delete) с моделями данных в базе данных,
    используя асинхронные запросы с помощью SQLAlchemy. Атрибуты: - model: класс модели данных, с которой будут
    выполняться операции CRUD Методы: - get_object(obj_id: int, session: AsyncSession) -> Union[None,
    model]: получает объект из базы данных по заданному идентификатору - get_all_objects(session: AsyncSession) ->
    List[model]: получает все объекты заданной модели из базы данных - create(obj_in, session: AsyncSession,
    user: Optional[User] = None) -> model: создает новый объект в базе данных на основе переданных данных - update(
    db_obj, obj_in, session: AsyncSession) -> model: обновляет данные объекта в базе данных на основе переданных
    данных - delete(db_obj, session: AsyncSession) -> model: удаляет объект из базы данных
    """

    def __init__(self, model):
        self.model = model

    async def get_object(
            self,
            obj_id: int,
            session: AsyncSession
    ):
        object_ = await session.execute(select(self.model).where(self.model.id == obj_id))
        return object_.scalars().first()

    async def get_all_objects(
            self,
            session: AsyncSession
    ):
        all_objects = await session.execute(select(self.model))
        return all_objects.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(
            self,
            db_obj,
            session: AsyncSession
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj
