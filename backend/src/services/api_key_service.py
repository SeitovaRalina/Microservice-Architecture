import secrets
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.errors.exceptions import NotFoundException
from src.schemas.internal import ApiKeyCreate
from src.repositories.api_key_repository import ApiKeyRepository
from src.models.api_key import ApiKey

class ApiKeyService:
    def __init__(self, db: AsyncSession):
        self.repo = ApiKeyRepository(db)

    async def generate_key(self, payload: ApiKeyCreate) -> ApiKey:
        while True:
            key = secrets.token_hex(32)  # 64 символа
            if not await self.repo.get_by_key(key):
                break

        api_key = ApiKey(
            key=key,
            description=payload.description,
            scopes=payload.scopes,
        )
        return await self.repo.create(api_key)

    async def get_valid_key(self, key: str) -> ApiKey:
        api_key = await self.repo.get_by_key(key)

        if not api_key or (api_key.expires_at and api_key.expires_at < datetime.now(timezone.utc)):
            raise NotFoundException("Недействительный или истёкший API ключ")

        return api_key
