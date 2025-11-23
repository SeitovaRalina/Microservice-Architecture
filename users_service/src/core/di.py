from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.repositories.user_repository import UserRepository
from src.services.auth_service import AuthService


async def get_auth_service(db: AsyncSession = Depends(get_db)) :
    return AuthService(db)

async def get_user_repository(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)
