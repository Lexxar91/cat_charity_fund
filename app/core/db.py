from app.core.config import settings

from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker


class PreBase:
    """
    Базовый класс для определения таблиц в базе данных с использованием SQLAlchemy.
    Определяет имя таблицы на основе имени класса, приведенного к нижнему регистру.
    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)
engine = create_async_engine(settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """
    Функция, создающая асинхронную сессию с базой данных и возвращающая ее через контекстный менеджер.
    Используется для выполнения асинхронных запросов к базе данных с помощью SQLAlchemy.
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
