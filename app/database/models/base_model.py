from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func

from app.database.db import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID')
    create_datetime = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.now(),
                             comment='UTC время создания')
    update_datetime = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.now(),
                             comment='UTC время обновления')
