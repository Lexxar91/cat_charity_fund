from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, Extra


class CharityBase(BaseModel):
    """
    Базовая модель для описания полей благотворительной организации.
    Атрибуты:
        ---------
        name : Optional[str]
            Название благотворительной организации (максимальная длина - 100 символов).
        description : Optional[str]
            Описание благотворительной организации.
        full_amount : Optional[PositiveInt]
            Полная сумма, необходимая для реализации благотворительного проекта.
    Конфигурация:
        -------------
        extra : str
            Действие при обнаружении дополнительных полей (forbid - запретить).
        min_anystr_length : int
            Минимальная длина для строковых полей.
    """
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityCreate(BaseModel):
    """
    Модель для создания благотворительной организации.
    Атрибуты:
        ---------
        name : str
            Название благотворительной организации (максимальная длина - 100 символов).
        description : str
            Описание благотворительной организации.
        full_amount : PositiveInt
            Полная сумма, необходимая для реализации благотворительного проекта.
    Конфигурация:
        -------------
        min_anystr_length : int
            Минимальная длина для строковых полей.
    """
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt

    class Config:
        min_anystr_length = 1


class CharityDB(CharityCreate):
    """
    Модель благотворительной организации, хранящаяся в базе данных.
    Атрибуты:
       ---------
       id : int
           Идентификатор благотворительной организации.
       invested_amount : int
           Сумма, уже вложенная в благотворительный проект.
       fully_invested : bool
           Флаг, указывающий, была ли полностью вложена полная сумма в проект.
       create_date : datetime
           Дата создания благотворительной организации.
       close_date : Optional[datetime]
           Дата закрытия благотворительной организации.
    Конфигурация:
       -------------
       orm_mode : bool
           Указание для Pydantic, что данный класс используется для работы с ORM.
    """
    id: int
    invested_amount: int = Field(0)
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityUpdate(CharityBase):
    """
    Модель для обновления благотворительной организации.
    Наследует атрибуты из класса `CharityBase`.
    """
    pass
