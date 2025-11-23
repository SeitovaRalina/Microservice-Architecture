from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from src.schemas.common import ORMBaseModel
from src.schemas.user import ProfileOut


class ArticleCreate(BaseModel):
    '''Схема создания статьи'''
    title: str = Field(..., min_length=3, max_length=300, example = "Заголовок статьи", description="Заголовок статьи")
    description: str = Field(..., min_length=3, max_length=500, example="Это краткое описание статьи.", description="Краткое описание статьи")
    body: str = Field(..., min_length=10, example="Это основной текст статьи.", description="Основной текст статьи")
    tagList: Optional[List[str]] = Field(default_factory=list, example= ["тег"], description="Список тегов статьи")

class ArticleUpdate(BaseModel):
    '''Схема обновления статьи'''
    title: Optional[str] = Field(None, min_length=3, max_length=300, example="Обновленный заголовок статьи", description="Новый заголовок статьи")
    description: Optional[str] = Field(None, min_length=3, max_length=500, example="Это обновленное краткое описание статьи.", description="Новое краткое описание статьи")
    body: Optional[str] = Field(None, min_length=10, example="Это обновленный основной текст статьи.", description="Новый основной текст статьи")
    tagList: Optional[List[str]] = Field(None, example=["обновленный_тег"], description="Обновленный список тегов статьи")

class ArticleOut(ORMBaseModel):
    '''Схема вывода статьи'''
    updated_at: datetime = Field(..., description="Дата и время последнего обновления", example="2023-10-05T14:48:00.000Z")
    title: str = Field(..., description="Заголовок статьи", example="Заголовок статьи")
    description: str = Field(..., description="Краткое описание статьи", example="Это краткое описание статьи.")
    body: str = Field(..., description="Основной текст статьи", example="Это основной текст статьи.")
    slug: str = Field(..., description="Уникальный slug статьи", example="zagolovok-stati")
    tagList: List[str] = Field(default_factory=list, description="Список тегов статьи", example=["тег"])
    author: Optional[ProfileOut] = Field(None, description="Автор статьи")
