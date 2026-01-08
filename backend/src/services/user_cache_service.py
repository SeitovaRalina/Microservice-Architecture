import os
from typing import Optional
import redis.asyncio as redis
import httpx
import logging

from src.schemas.profile import ProfileOut

logger = logging.getLogger(__name__)

class UserCacheService:
    def __init__(self):
        self.redis = redis.from_url(
            os.getenv("REDIS_URL", "redis://redis:6379/0"),
            encoding="utf-8",
            decode_responses=True
        )
        self.users_service_url = os.getenv("USERS_SERVICE_URL", "http://users_service:8000")
        self.cache_ttl = int(os.getenv("PROFILE_CACHE_TTL", "86400"))

    async def get_profile(self, user_id: int) -> ProfileOut:
        cache_key = f"user:profile:{user_id}"

        cached = await self.redis.get(cache_key)
        if cached:
            logger.info(f"ATTENTION Cache hit for user {user_id}")
            return ProfileOut.model_validate_json(cached)

        profile_data = await self._fetch_from_users_service(user_id)
        if profile_data:
            await self.redis.setex(
                cache_key,
                self.cache_ttl,
                profile_data.model_dump_json()
            )
            return profile_data

        return ProfileOut(
            username=f"user_{user_id}",
            bio=None,
            image_url=None
        )

    async def _fetch_from_users_service(self, user_id: int) -> Optional[ProfileOut]:
        try:
            async with httpx.AsyncClient(timeout=1.5) as client:
                response = await client.get(
                    f"http://users_service:8000/api/users/{user_id}/profile"
                )
                if response.status_code == 200:
                    data = response.json()
                    return ProfileOut(**data)
                elif response.status_code == 404:
                    profile = ProfileOut(username="deleted_user", bio=None, image_url=None)
                    await self.redis.setex(f"user:profile:{user_id}", self.cache_ttl, profile.model_dump_json())
                    return profile
        except Exception as e:
            logger.warning(f"Users_service unreachable for user {user_id}: {e}")
        return None

    async def invalidate(self, user_id: int):
        deleted = await self.redis.delete(f"user:profile:{user_id}")
        logger.info(f"ATTENTION Invalidated profile cache for user {user_id} (keys deleted: {deleted})")

    async def close(self):
        await self.redis.close()
