from fastapi import Depends
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials
from typing import List, Optional

from src.core.utils.security import security
from src.core.di import get_api_key_service
from src.services.api_key_service import ApiKeyService
from src.models.api_key import ApiKey
from src.core.errors.exceptions import UnauthorizedException, ForbiddenException

header_scheme = APIKeyHeader(name="Authorization", auto_error=False)

class APIKeyChecker:
    def __init__(self, required_scopes: List[str]):
        self.required_scopes = required_scopes

    async def __call__(
        self,
        auth_header: Optional[str] = Depends(header_scheme),
        api_key_service: ApiKeyService = Depends(get_api_key_service),
    ) -> ApiKey:
        if not auth_header:
            raise UnauthorizedException("Отсутствует заголовок Authorization")

        try:
            scheme, token = auth_header.split(" ", 1)
        except ValueError:
            raise UnauthorizedException("Неверный формат заголовка. Ожидается 'Token <key>'")

        if scheme.lower() == "bearer":
            raise ForbiddenException("JWT-токены запрещены на внутренних эндпоинтах")

        if scheme.lower() != "token":
            raise UnauthorizedException(f"Ожидается схема 'Token', получено: {scheme}")

        api_key = await api_key_service.get_valid_key(token)

        if self.required_scopes:
            missing = set(self.required_scopes) - set(api_key.scopes or [])
            if missing:
                raise ForbiddenException(f"Недостаточно прав. Требуются scopes: {missing}")

        return api_key

require_moderation_key = APIKeyChecker(["moderate", "reject"])
require_preview_key    = APIKeyChecker(["preview"])
require_publish_key    = APIKeyChecker(["publish"])
require_error_key      = APIKeyChecker(["error"])
require_profile_key    = APIKeyChecker(["profile"])