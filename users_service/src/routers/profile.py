from fastapi import APIRouter, Depends

from src.schemas.profile import ProfileOut
from src.controllers import profile as profile_ctrl


router = APIRouter(prefix="/api/users", tags=["profile"])


@router.get("/{user_id}/profile", response_model=ProfileOut,
            summary="Получить публичный профиль пользователя", description="Возвращает только публичную информацию о пользователе.")
async def get_public_profile(payload: ProfileOut = Depends(profile_ctrl.get_public_profile)):
    return payload
