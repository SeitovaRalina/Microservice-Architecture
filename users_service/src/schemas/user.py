from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.models.user import User
from src.schemas.common import ORMBaseModel


class UserCreate(BaseModel):
    '''Схема регистрации пользователя'''
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    username: str = Field(..., min_length=3, max_length=150, pattern=r"^[a-zA-Z0-9_]+$", example="user", description="Имя пользователя (может содержать английские буквы, цифры и подчеркивания, уникальное)")
    password: str = Field(..., min_length=6, example="password", description="Пароль пользователя (минимум 6 символов)")
    bio: Optional[str] = Field(None, example="Привет! Я новый пользователь.", description="Краткая биография пользователя")
    image_url: Optional[str] = Field(None, example="https://example.com/avatar.jpg", description="URL аватара пользователя")

class UserLogin(BaseModel):
    '''Схема входа пользователя'''
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=6, example="password", description="Пароль")

class UserUpdate(BaseModel):
    '''Схема обновления данных пользователя'''
    email: Optional[EmailStr] = Field(None, description="Новая электронная почта")
    username: Optional[str] = Field(None, min_length=3, max_length=150, pattern=r"^[a-zA-Z0-9_]+$", example="new_user", description="Новое имя пользователя (может содержать английские буквы, цифры и подчеркивания, уникальное)")
    password: Optional[str] = Field(None, min_length=6, example="newpassword", description="Новый пароль (минимум 6 символов)")
    bio: Optional[str] = Field(None, example="Это моя обновленная биография.", description="Обновленная биография")
    image_url: Optional[str] = Field(None, example="https://example.com/new_avatar.jpg", description="Новый URL аватара")

class UserOut(ORMBaseModel):
    '''Схема вывода данных авторизованного пользователя'''
    updated_at: datetime = Field(..., description="Дата и время последнего обновления", example="2023-10-05T14:48:00.000Z")
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    username: str = Field(..., description="Имя пользователя", example="user")
    bio: Optional[str] = Field(None, description="Краткая биография пользователя", example="Привет! Я новый пользователь.")
    image_url: Optional[str] = Field(None, description="URL аватара пользователя", example="https://example.com/avatar.jpg")

class TokenResponse(BaseModel):
    '''Схема ответа с JWT токеном'''
    access_token: str = Field(..., description="JWT токен доступа", example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field('bearer', description="Тип токена", example="bearer")
