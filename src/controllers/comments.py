from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.comment import Comment
from src.models.article import Article
from src.models.user import User
from src.schemas.comment import CommentCreate
from src.core.errors.exceptions import NotFoundException, ForbiddenException

async def add_comment(db: AsyncSession, article: Article, current_user: User, comment_in: CommentCreate) -> Comment:
    comment = Comment(
        body=comment_in.body,
        author=current_user,
        article=article
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment

async def get_comments(db: AsyncSession, article: Article) -> List[Comment]:
    q = await db.execute(
        select(Comment).where(Comment.article_id == article.id).order_by(Comment.created_at.asc())
    )
    return q.scalars().all()

async def delete_comment(db: AsyncSession, comment_id: int, current_user: User):
    q = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = q.scalar_one_or_none()
    if not comment:
        raise NotFoundException("Комментарий не найден")
    if comment.author_id != current_user.id:
        raise ForbiddenException("Нет доступа для удаления этого комментария")
    await db.delete(comment)
    await db.commit()
