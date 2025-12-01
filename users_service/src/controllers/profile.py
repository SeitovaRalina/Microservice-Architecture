from fastapi import Depends
from fastapi.params import Path

from src.core.di import get_auth_service
from src.schemas.profile import ProfileOut
from src.services.auth_service import AuthService


async def get_public_profile(
    user_id: int = Path(..., description="ID пользователя"),
    user_service: AuthService = Depends(get_auth_service),
) -> ProfileOut:
    user = await user_service.get_user_by_id(user_id)
    return ProfileOut.model_validate(user)
