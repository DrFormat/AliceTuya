from typing import Any, Generic, Optional, Type, TypeVar

import sqlalchemy
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import Base
from app.core.exceptions import NotFoundException, ConflictException

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self.model = model
        self.db_session = db_session

    async def objs_list(self, **kwargs) -> list[ModelType]:
        query = select(self.model)
        result = await self.db_session.execute(query)
        objs: list[ModelType] = result.scalars().all()
        return objs

    async def get(self, _id: Any) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == _id)
        result = await self.db_session.execute(query)
        obj: Optional[ModelType] = result.scalars().one_or_none()
        return obj

    async def get_external(self, _id: Any) -> Optional[ModelType]:
        query = select(self.model).where(self.model.external_id == _id)
        result = await self.db_session.execute(query)
        obj: Optional[ModelType] = result.scalars().one_or_none()
        return obj

    async def create(self, obj: CreateSchemaType) -> ModelType:
        db_obj: ModelType = self.model(**obj.dict())
        self.db_session.add(db_obj)
        try:
            await self.db_session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            await self.db_session.rollback()
            if "duplicate key" in str(e):
                raise ConflictException()
            else:
                raise e
        return db_obj

    async def update(self, _id: Any, obj: UpdateSchemaType) -> Optional[ModelType]:
        db_obj = await self.db_session.get(self.model, _id)
        if db_obj:
            for column, value in obj.dict(exclude_unset=True).items():
                setattr(db_obj, column, value)
            await self.db_session.commit()
            return db_obj
        else:
            raise NotFoundException()

    async def delete(self, _id: Any) -> Optional[ModelType]:
        db_obj = await self.db_session.get(self.model, _id)
        if db_obj is None:
            raise NotFoundException()
        await self.db_session.delete(db_obj)
        await self.db_session.commit()
        return db_obj

    async def set_external_id(self, _id: Any, external_id: Any) -> Optional[ModelType]:
        db_obj = await self.db_session.get(self.model, _id)
        if db_obj is None:
            raise NotFoundException()
        db_obj.external_id = str(external_id)
        await self.db_session.commit()
        return db_obj
