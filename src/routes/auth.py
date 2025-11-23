from fastapi import APIRouter, Depends

from src.schemas.user import UserOut, TokenResponse
from src.schemas.common import DeleteResponse
from src.controllers import auth as auth_ctrl


router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("", response_model=UserOut, status_code=201,
             summary="Зарегистрировать нового пользователя", description="Создает нового пользователя в системе.")
async def register(payload: UserOut = Depends(auth_ctrl.register_user)):
    return payload

@router.post("/login", response_model=TokenResponse,
             summary="Войти в систему", description="Аутентифицирует пользователя и возвращает токен доступа.")
async def login(payload: TokenResponse = Depends(auth_ctrl.login_user)):
    return payload

@router.get("/me", response_model=UserOut,
             summary="Получить текущего пользователя", description="Возвращает информацию о текущем аутентифицированном пользователе.")
async def get_current_user(payload: UserOut = Depends(auth_ctrl.get_current_user_profile)):
    return payload

@router.put("/me", response_model=UserOut,
             summary="Обновить текущего пользователя", description="Обновляет информацию о текущем аутентифицированном пользователе.")
async def update_user(payload: UserOut = Depends(auth_ctrl.update_current_user)):
    return payload

@router.delete("/me", response_model=DeleteResponse,
               summary="Удалить текущего пользователя", description="Удаляет текущего аутентифицированного пользователя из системы.")
async def delete_user(payload: DeleteResponse = Depends(auth_ctrl.delete_current_user)):
    return payload
