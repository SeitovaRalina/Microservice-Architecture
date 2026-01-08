from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.api_key import ApiKey

class ApiKeyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_key(self, key: str) -> Optional[ApiKey]:
        result = await self.session.execute(select(ApiKey).where(ApiKey.key == key))
        return result.scalar_one_or_none()

    async def create(self, api_key: ApiKey) -> ApiKey:
        self.session.add(api_key)
        await self.session.flush([api_key])
        return api_key
