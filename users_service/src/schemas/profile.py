from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ProfileOut(BaseModel):
    '''Схема вывода данных публичного профиля пользователя'''
    username: str = Field(..., description="Имя пользователя", example="user")
    bio: Optional[str] = Field(None, description="Краткая биография пользователя", example="Привет! Я новый пользователь.")
    image_url: Optional[str] = Field(None, description="URL аватара пользователя", example="https://example.com/avatar.jpg")

    model_config = ConfigDict(from_attributes=True)
