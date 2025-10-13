from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.controllers.auth import get_user_by_id
from src.models.user import User
from src.db import get_db
from src.core.utils.security import security, verify_token
from src.core.errors.exceptions import UnauthorizedException


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)) -> User:
    if credentials is None:
        raise UnauthorizedException("Отсутствует токен авторизации")

    token = credentials.credentials
    user_id = verify_token(token)
    if user_id is None:
        raise UnauthorizedException("Неверный токен авторизации или срок его действия истёк")

    user = await get_user_by_id(db, user_id)
    if user is None or user.is_deleted:
        raise UnauthorizedException("Пользователь не найден или удален")
    return user
