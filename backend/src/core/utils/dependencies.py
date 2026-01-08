from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from src.services.api_key_service import ApiKeyService
from src.core.di import get_api_key_service
from src.core.utils.security import security, verify_token
from src.core.errors.exceptions import UnauthorizedException, ForbiddenException


async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    if credentials is None:
        raise UnauthorizedException("Отсутствует токен авторизации")

    token = credentials.credentials
    user_id = verify_token(token)
    if user_id is None:
        raise UnauthorizedException("Неверный токен авторизации или срок его действия истёк")
    return user_id

async def get_internal_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    api_key_service: ApiKeyService = Depends(get_api_key_service)
) -> str:
    if credentials is None:
        raise UnauthorizedException("Отсутствует токен авторизации")

    scheme, token = credentials.scheme.lower(), credentials.credentials

    if scheme == "bearer":
        raise ForbiddenException("Недопустимая схема авторизации для внутреннего API ключа")
    elif scheme != "api_key":
        raise UnauthorizedException("Неверная схема авторизации, ожидается 'Token <key>'")

    if not await api_key_service.validate_key(token):
        raise UnauthorizedException("Недействительный или истёкший API ключ")

    return token
