from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.schemas.user import UserCreate, UserLogin, UserOut, TokenResponse, UserUpdate
from src.schemas.common import DeleteResponse
from src.controllers import auth as auth_ctrl
from src.core.utils.security import create_access_token
from src.core.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("", response_model=UserOut, status_code=201,
             summary="Зарегистрировать нового пользователя", description="Создает нового пользователя в системе.")
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    return await auth_ctrl.create_user(db, user_in)

@router.post("/login", response_model=TokenResponse,
             summary="Войти в систему", description="Аутентифицирует пользователя и возвращает токен доступа.")
async def login(user_login: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await auth_ctrl.authenticate_user(db, user_login)
    access_token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=access_token)

@router.get("", response_model=UserOut,
             summary="Получить текущего пользователя", description="Возвращает информацию о текущем аутентифицированном пользователе.")
async def get_current_user(user = Depends(get_current_user)):
    return user

@router.put("", response_model=UserOut,
             summary="Обновить текущего пользователя", description="Обновляет информацию о текущем аутентифицированном пользователе.")
async def update_user(user_in: UserUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await auth_ctrl.update_user(db, current_user, user_in)

@router.delete("", response_model=DeleteResponse,
               summary="Удалить текущего пользователя", description="Удаляет текущего аутентифицированного пользователя из системы.")
async def delete_user(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    await auth_ctrl.delete_user(db, current_user)
    return {"detail": "User deleted"}
