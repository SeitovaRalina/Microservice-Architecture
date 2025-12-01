from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.services.article_service import ArticleService
from src.services.comment_service import CommentService
from src.services.user_cache_service import UserCacheService


async def get_article_service(db: AsyncSession = Depends(get_db)):
    return ArticleService(db)

async def get_comment_service(db: AsyncSession = Depends(get_db)):
    return CommentService(db)

async def get_user_cache_service():
    return UserCacheService()
