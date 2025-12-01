from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from src.core.di import get_user_cache_service

router = APIRouter(prefix="/internal", tags=["internal"])

class InvalidateCachePayload(BaseModel):
    user_id: int = Field(..., gt=0)
    reason: str = Field(default="unknown", examples=["profile_updated", "account_deleted"])

@router.post("/invalidate-profile-cache")
async def invalidate_profile_cache(
    payload: InvalidateCachePayload,
    cache_service = Depends(get_user_cache_service)
):
    await cache_service.invalidate(payload.user_id)
    return {"status": "ok", "user_id": payload.user_id, "reason": payload.reason}