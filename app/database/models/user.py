from sqlalchemy import Column, String

from .base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    username = Column(String, nullable=True, comment='username')
    password = Column(String, nullable=True, comment='password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

