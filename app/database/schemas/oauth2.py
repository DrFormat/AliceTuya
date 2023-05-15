import time
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator

from app import database


class OAuth2ApplicationBase(BaseModel):
    client_id: str = Field(title=database.OAuth2Application.client_id.comment)
    client_secret: Optional[str] = Field(title=database.OAuth2Application.client_secret.comment)
    client_type: Optional[str] = Field(title=database.OAuth2Application.client_type.comment)
    authorization_grant_type: Optional[str] = Field(title=database.OAuth2Application.authorization_grant_type.comment)
    name: Optional[str] = Field(title=database.OAuth2Application.name.comment)
    algorithm: Optional[str] = Field(title=database.OAuth2Application.algorithm.comment)
    redirect_uris: Optional[str] = Field(title=database.OAuth2Application.redirect_uris.comment)

    @validator('redirect_uris')
    def redirect_uris_set(cls, v):
        return v.split(' ')


class OAuth2Application(OAuth2ApplicationBase):
    id: int = Field(title=database.OAuth2Application.id.comment)
    create_datetime: datetime = Field(title=database.OAuth2Application.create_datetime.comment)
    update_datetime: datetime = Field(title=database.OAuth2Application.update_datetime.comment)

    class Config:
        title = 'Application'
        orm_mode = True


class OAuth2ApplicationCreateUpdate(OAuth2ApplicationBase):
    class Config:
        title = 'Создание/Обновление Application'


class OAuth2AuthorizationCodeBase(BaseModel):
    code: str = Field()
    client_id: str = Field()
    redirect_uri: str = Field(default='')
    response_type: Optional[str] = Field(default='')
    scope: Optional[str] = Field(default='')
    nonce: Optional[str] = Field('')
    auth_time: int = Field(int(time.time()))
    code_challenge: Optional[str] = Field('')
    code_challenge_method: Optional[str] = Field('')
    user_id: int = Field()


class OAuth2AuthorizationCode(OAuth2AuthorizationCodeBase):
    id: int = Field(title=database.OAuth2AuthorizationCode.id.comment)
    create_datetime: datetime = Field(title=database.OAuth2AuthorizationCode.create_datetime.comment)
    update_datetime: datetime = Field(title=database.OAuth2AuthorizationCode.update_datetime.comment)

    class Config:
        title = 'OAuth2AuthorizationCode'
        orm_mode = True


class OAuth2AuthorizationCodeCreateUpdate(OAuth2AuthorizationCodeBase):
    class Config:
        title = 'Создание/Обновление OAuth2AuthorizationCode'


class OAuth2TokenBase(BaseModel):
    client_id: str = Field(max_length=48)
    token_type: str = Field(max_length=40)
    access_token: str = Field(max_length=255)
    refresh_token: str = Field(max_length=255)
    scope: Optional[str] = Field(default='')
    issued_at: int = Field(int(time.time()))
    access_token_revoked_at: int = Field(0)
    refresh_token_revoked_at: int = Field(0)
    expires_in: int = Field(0)
    user_id: int = Field()

    def is_revoked(self) -> int | bool:
        return self.access_token_revoked_at or self.refresh_token_revoked_at


class OAuth2Token(OAuth2TokenBase):
    id: int = Field(title=database.OAuth2Token.id.comment)
    create_datetime: datetime = Field(title=database.OAuth2Token.create_datetime.comment)
    update_datetime: datetime = Field(title=database.OAuth2Token.update_datetime.comment)

    class Config:
        title = 'OAuth2AuthorizationCode'
        orm_mode = True


class OAuth2TokenCreateUpdate(OAuth2TokenBase):
    class Config:
        title = 'Создание/Обновление OAuth2AuthorizationCode'
