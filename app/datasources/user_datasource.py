from typing import Any, Optional

from sqlalchemy import select

from app.database import User
from app.database.base_service import BaseService
from app.database.schemas.user import UserCreateUpdate


class UserDatasource(BaseService[User, UserCreateUpdate, UserCreateUpdate]):
    async def get_by_username(self, username: Any) -> Optional[User]:
        query = select(User).where(User.username == username)
        result = await self.db_session.execute(query)
        obj: Optional[User] = result.scalars().one_or_none()
        return obj
