from datetime import datetime
from typing import Generic, List, TypeVar
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar('T')

class ListResponse(BaseModel, Generic[T]):
    items: List[T] = Field(..., description="Список элементов")

class PaginationMeta(BaseModel):
    '''Метаданные для пагинации'''
    page: int = Field(..., ge=1, description="Номер текущей страницы", example=1)
    per_page: int = Field(..., ge=1, le=100, description="Количество элементов на странице", example=20)
    total_items: int = Field(..., ge=0, description="Общее количество элементов", example=100)
    total_pages: int = Field(..., ge=0, description="Общее количество страниц", example=5)

class PaginatedResponse(ListResponse):
    '''Схема ответа с пагинацией'''
    meta: PaginationMeta = Field(..., description="Метаданные пагинации")

class DeleteResponse(BaseModel):
    detail: str = Field(..., description="Сообщение об успешном удалении", example="Entity deleted")

class ORMBaseModel(BaseModel):
    '''Схема базовой модели с ORM совместимостью'''
    id : int = Field(..., description="Уникальный идентификатор", example=1)
    created_at: datetime = Field(..., description="Дата и время создания", example="2023-10-05T14:48:00.000Z")

    model_config = ConfigDict(from_attributes=True)
