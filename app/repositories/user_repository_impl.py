from fastapi import Depends
from pydantic import parse_obj_as
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

import app.database as db
import app.database.schemas as schema
from app.core.exceptions import NotFoundException
from app.core.repository import Repository
from app.database.db import get_session
from app.datasources.user_datasource import UserDatasource


class UserRepositoryImpl(Repository):
    datasource: UserDatasource

    def __init__(self, request: Request, db_session: AsyncSession):
        self.request = request
        self.datasource = UserDatasource(db_session=db_session, model=db.User)

    async def objs_list(self, **kwargs) -> list[schema.User]:
        data = await self.datasource.objs_list(**kwargs)
        return parse_obj_as(list[schema.User], data)

    async def get(self, _id: int) -> schema.User:
        obj = await self.datasource.get(_id)
        if obj is None:
            raise NotFoundException()
        return parse_obj_as(schema.User, obj)

    async def get_by_username(self, username: str) -> schema.User:
        obj = await self.datasource.get_by_username(username)
        if obj is None:
            raise NotFoundException()
        return parse_obj_as(schema.User, obj)

    async def create(self, data) -> schema.User:
        obj = await self.datasource.create(data)
        return parse_obj_as(schema.User, obj)

    async def update(self, _id, data) -> schema.User:
        obj = await self.datasource.update(_id, data)
        if obj:
            return parse_obj_as(schema.User, obj)
        else:
            raise NotFoundException('User')

    async def delete(self, _id: int) -> schema.Status:
        obj = await self.datasource.delete(_id)
        if obj:
            return schema.Status(status='Ok')
        else:
            raise NotFoundException('User')


async def get_user_repo(request: Request, db_session: AsyncSession = Depends(get_session)) -> UserRepositoryImpl:
    return UserRepositoryImpl(request, db_session)
