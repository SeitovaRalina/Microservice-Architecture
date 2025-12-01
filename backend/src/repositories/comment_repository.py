from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.comment import Comment
from src.models.article import Article


class CommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, comment: Comment) -> Comment:
        self.session.add(comment)
        await self.session.flush([comment])
        return comment

    async def get_by_id(self, comment_id: int) -> Optional[Comment]:
        result = await self.session.execute(
            select(Comment).where(Comment.id == comment_id)
        )
        return result.scalar_one_or_none()

    async def get_by_article(self, article: Article) -> List[Comment]:
        result = await self.session.execute(
            select(Comment)
            .where(Comment.article_id == article.id)
            .order_by(Comment.created_at.asc())
        )
        return result.scalars().all()

    async def delete(self, comment: Comment) -> None:
        await self.session.delete(comment)
        await self.session.flush()
