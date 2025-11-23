from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.repositories.user_repository import UserRepository
from src.services.auth_service import AuthService
from src.services.article_service import ArticleService
from src.services.comment_service import CommentService


async def get_article_service(db: AsyncSession = Depends(get_db)):
    return ArticleService(db)

async def get_auth_service(db: AsyncSession = Depends(get_db)) :
    return AuthService(db)

async def get_comment_service(db: AsyncSession = Depends(get_db)):
    return CommentService(db)


async def get_user_repository(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)
