from datetime import datetime
from typing import Optional
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
    expires_at: Optional[datetime] = Field(None, description="Дата и время истечения срока действия ключа", example="2024-12-31T23:59:59Z")

class ApiKeyResponse(BaseModel):
    '''Схема ответа с информацией об API ключе (админский эндпоинт)'''
    id: int
    key: str
    description: str
    expires_at: Optional[datetime]
