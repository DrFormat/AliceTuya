import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import config

if 'starlette' in sys.modules:
    engine = create_async_engine(config.DB_DSN, echo=config.DEBUG, connect_args={'check_same_thread': False})
else:
    engine = create_engine(config.DB_DSN, echo=config.DEBUG)

Base = declarative_base()


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
