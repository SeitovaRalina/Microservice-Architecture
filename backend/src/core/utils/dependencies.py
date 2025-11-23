from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from src.core.di import get_user_repository
from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.core.utils.security import security, verify_token
from src.core.errors.exceptions import UnauthorizedException


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                           repo: UserRepository = Depends(get_user_repository)) -> User:
    if credentials is None:
        raise UnauthorizedException("Отсутствует токен авторизации")

    token = credentials.credentials
    user_id = verify_token(token)
    if user_id is None:
        raise UnauthorizedException("Неверный токен авторизации или срок его действия истёк")

    user = await repo.get_by_id(user_id)
    if user is None:
        raise UnauthorizedException("Пользователь не найден")
    if user.is_deleted:
        raise UnauthorizedException("Пользователь удалён")
    return user
