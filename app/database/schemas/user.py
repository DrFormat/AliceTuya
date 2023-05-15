from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app import database


class UserBase(BaseModel):
    username: str = Field(title=database.User.username.comment)
    password: str = Field(title=database.User.password.comment)


class User(UserBase):
    id: int = Field(title=database.User.id.comment)
    create_datetime: datetime = Field(title=database.User.create_datetime.comment)
    update_datetime: datetime = Field(title=database.User.update_datetime.comment)

    class Config:
        title = 'User'
        orm_mode = True


class UserCreateUpdate(UserBase):
    class Config:
        title = 'Создание/Обновление User'

