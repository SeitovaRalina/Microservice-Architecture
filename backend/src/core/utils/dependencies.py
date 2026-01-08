from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from src.core.utils.security import security, verify_token
from src.core.errors.exceptions import UnauthorizedException


async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    if credentials is None:
        raise UnauthorizedException("Отсутствует токен авторизации")

    token = credentials.credentials
    user_id = verify_token(token)
    if user_id is None:
        raise UnauthorizedException("Неверный токен авторизации или срок его действия истёк")
    return user_id
