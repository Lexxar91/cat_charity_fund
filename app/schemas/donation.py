from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, Extra


class DonationCreate(BaseModel):
    """
    Модель для создания новой записи о пожертвовании.
    Атрибуты:
        ---------
        full_amount : PositiveInt
            Сумма пожертвования (целое положительное число).
        comment : Optional[str], необязательный
            Комментарий к пожертвованию.
    """
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationUser(DonationCreate):
    """
    Модель записи о пожертвовании с дополнительными атрибутами,
    предназначенными для пользовательского интерфейса.
    """
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationCreate):
    """
    Модель записи о пожертвовании с дополнительными атрибутами,
    предназначенными для сохранения в базе данных.
    Атрибуты:
         ---------
        id : int
            Уникальный идентификатор записи о пожертвовании.
        create_date : datetime
            Дата и время создания записи о пожертвовании.
        user_id : int, необязательный
            Идентификатор пользователя, совершившего пожертвование.
        full_amount : PositiveInt
            Сумма пожертвования (целое положительное число).
        comment : Optional[str], необязательный
            Комментарий к пожертвованию.
        invested_amount : int
            Сумма, которую удалось привлечь на момент создания записи о пожертвовании (целое число).
        fully_invested : bool
            Флаг, указывающий, была ли достигнута целевая сумма для пожертвования.
        close_date : Optional[datetime], необязательный
            Дата и время, когда была достигнута целевая сумма для пожертвования.
    """
    id: int
    create_date: datetime
    user_id: int = None
    invested_amount: int = Field(0)
    fully_invested: bool = Field(False)
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
