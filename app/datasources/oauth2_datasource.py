from typing import Any, Optional

import sqlalchemy
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException, ConflictException
from app.database import OAuth2AuthorizationCode, OAuth2Application
from app.database.db import get_session
from app.database.models.oauth2 import OAuth2Token
from app.database import schemas


class OAuth2Datasource:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_app_by_client_id(self, client_id: Any) -> Optional[OAuth2Application]:
        query = select(OAuth2Application).where(OAuth2Application.client_id == client_id)
        result = await self.db_session.execute(query)
        obj: Optional[OAuth2Application] = result.scalars().one_or_none()
        return obj

    async def get_authorization_code(self, code: Any) -> Optional[OAuth2AuthorizationCode]:
        query = select(OAuth2AuthorizationCode).where(OAuth2AuthorizationCode.code == code)
        result = await self.db_session.execute(query)
        obj: Optional[OAuth2AuthorizationCode] = result.scalars().one_or_none()
        return obj

    async def create_authorization_code(self,
                                        obj: schemas.OAuth2AuthorizationCodeCreateUpdate) -> OAuth2AuthorizationCode:
        db_obj = OAuth2AuthorizationCode(**obj.dict())
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

    async def update_authorization_code(self, _id: Any, obj: schemas.OAuth2AuthorizationCodeCreateUpdate) -> \
            Optional[OAuth2AuthorizationCode]:
        db_obj: Optional[OAuth2AuthorizationCode] = await self.db_session.get(OAuth2AuthorizationCode, _id)
        if db_obj:
            for column, value in obj.dict(exclude_unset=True).items():
                setattr(db_obj, column, value)
            await self.db_session.commit()
            return db_obj
        else:
            raise NotFoundException()

    async def delete_authorization_code(self, _id: Any) -> Optional[OAuth2AuthorizationCode]:
        db_obj: Optional[OAuth2AuthorizationCode] = await self.db_session.get(OAuth2AuthorizationCode, _id)
        if db_obj is None:
            raise NotFoundException()
        await self.db_session.delete(db_obj)
        await self.db_session.commit()
        return db_obj

    async def get_token(self, token: Any, token_type: str = 'access_token') -> Optional[OAuth2Token]:
        query = select(OAuth2Token)
        if token_type == 'access_token':
            query = query.where(OAuth2Token.access_token == token)
        elif token_type == 'refresh_token':
            query = query.where(OAuth2Token.refresh_token == token)
        result = await self.db_session.execute(query)
        obj: Optional[OAuth2AuthorizationCode] = result.scalars().one_or_none()
        return obj

    async def create_token(self, obj: schemas.OAuth2TokenCreateUpdate) -> OAuth2Token:
        db_obj = OAuth2Token(**obj.dict())
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

    async def update_token(self, _id: Any, obj: schemas.OAuth2Token | schemas.OAuth2TokenCreateUpdate) -> Optional[OAuth2Token]:
        db_obj: Optional[OAuth2Token] = await self.db_session.get(OAuth2Token, _id)
        if db_obj:
            for column, value in obj.dict(exclude_unset=True).items():
                setattr(db_obj, column, value)
            await self.db_session.commit()
            return db_obj
        else:
            raise NotFoundException()

    async def delete_token(self, _id: Any) -> Optional[OAuth2Token]:
        db_obj: Optional[OAuth2Token] = await self.db_session.get(OAuth2Token, _id)
        if db_obj is None:
            raise NotFoundException()
        await self.db_session.delete(db_obj)
        await self.db_session.commit()
        return db_obj


async def get_oauth2_ds(db_session: AsyncSession = Depends(get_session)) -> OAuth2Datasource:
    return OAuth2Datasource(db_session)
