from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush([user])
        await self.session.refresh(user)
        return user

    async def update(self, user: User) -> User:
        await self.session.flush([user])
        await self.session.refresh(user)
        return user

    async def soft_delete(self, user: User) -> None:
        user.is_deleted = True
        user.deleted_at = datetime.now(timezone.utc)
        await self.session.flush([user])
        await self.session.refresh(user)
