from authlib.integrations.sqla_oauth2 import OAuth2AuthorizationCodeMixin, OAuth2TokenMixin
from sqlalchemy.orm import relationship

from app.database.models.base_model import BaseModel
from sqlalchemy import Column, String, Text, Integer, ForeignKey

from .base_model import BaseModel


class OAuth2Application(BaseModel):
    __tablename__ = 'oauth2_applications'

    client_id = Column(String(length=100), index=True)
    client_secret = Column(String(length=255), index=True, nullable=True)
    client_type = Column(String(length=32))
    authorization_grant_type = Column(String(length=32))
    name = Column(String(length=255))
    algorithm = Column(String(length=5))
    redirect_uris = Column(Text, nullable=True)


class OAuth2AuthorizationCode(BaseModel, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'oauth2_authorization_code'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    application_id = Column(Integer, ForeignKey('oauth2_applications.id', ondelete='CASCADE'))
    # user = relationship('User')
    # application = relationship('Application')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)


class OAuth2Token(BaseModel, OAuth2TokenMixin):
    __tablename__ = 'oauth2_token'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    application_id = Column(Integer, ForeignKey('oauth2_applications.id', ondelete='CASCADE'))
    # user = relationship('User')
    # application = relationship('Application')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
