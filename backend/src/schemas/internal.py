from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class InvalidateCachePayload(BaseModel):
    """Схема для инвалидирования кэша профиля (внутренний эндпоинт)"""
    user_id: int = Field(..., gt=0)
    reason: str = Field(default="unknown", examples=["profile_updated", "account_deleted"])


class ArticlePreviewCreate(BaseModel):
    """Схема для сохранения превью статьи (внутренний эндпоинт)"""
    preview_url: Optional[str] = Field(None, max_length=500, example="https://example.com/preview.jpg", description="URL превью изображения статьи")

class SuccessResponse(BaseModel):
    '''Схема ответа на успешную операцию (внутренний эндпоинт)'''
    detail: str = Field(..., description="Сообщение об успешной операции", example="Operation successful")


class ApiKeyCreate(BaseModel):
    '''Схема создания API ключа (админский эндпоинт)'''
    description: str = Field(..., example="all-internal-workers")
    scopes: List[str] = Field(..., example=["moderate", "reject"])

class ApiKeyResponse(BaseModel):
    '''Схема ответа с информацией об API ключе (админский эндпоинт)'''
    id: int
    key: str
    description: str
    scopes: List[str]
    expires_at: Optional[datetime]
