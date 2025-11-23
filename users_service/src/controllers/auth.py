from fastapi import Depends

from src.core.di import get_auth_service
from src.services.auth_service import AuthService
from src.schemas.user import UserCreate, UserLogin, UserUpdate, UserOut, TokenResponse
from src.schemas.common import DeleteResponse
from src.core.utils.security import create_access_token
from src.core.utils.dependencies import get_current_user
from src.models.user import User


async def register_user(
    user_in: UserCreate,
    service: AuthService = Depends(get_auth_service)
) -> UserOut:
    user = await service.register(user_in)
    return UserOut.model_validate(user)


async def login_user(
    user_login: UserLogin,
    service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    user = await service.authenticate(user_login)
    access_token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=access_token)

async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
) -> UserOut:
    return UserOut.model_validate(current_user)

async def update_current_user(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service)
) -> UserOut:
    updated_user = await service.update_profile(current_user, user_in)
    return UserOut.model_validate(updated_user)

async def delete_current_user(
    current_user: User = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service)
) -> DeleteResponse:
    await service.delete_account(current_user)
    return DeleteResponse(detail="User deleted")
