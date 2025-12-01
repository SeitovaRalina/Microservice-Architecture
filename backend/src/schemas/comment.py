from typing import Optional
from pydantic import BaseModel, Field

from src.schemas.common import ORMBaseModel
from src.schemas.user import ProfileOut


class CommentCreate(BaseModel):
    '''Схема создания комментария'''
    body: str = Field(..., min_length=1, example="Это комментарий к статье.", description="Текст комментария")

class CommentOut(ORMBaseModel):
    '''Схема вывода комментария'''
    id : int = Field(..., description="Уникальный идентификатор", example=1)
    body: str = Field(..., description="Текст комментария", example="Это комментарий к статье.")
    author: Optional[ProfileOut] = Field(None, description="Автор комментария")
