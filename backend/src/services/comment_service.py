from sqlalchemy.ext.asyncio import AsyncSession

from src.models.comment import Comment
from src.models.article import Article
from src.schemas.comment import CommentCreate
from src.repositories.comment_repository import CommentRepository
from src.core.errors.exceptions import NotFoundException, ForbiddenException


class CommentService:
    def __init__(self, db: AsyncSession):
        self.repo = CommentRepository(db)

    async def add_comment(
        self,
        article: Article,
        current_user_id: int,
        data: CommentCreate
    ) -> Comment:
        comment = Comment(
            body=data.body.strip(),
            author_id=current_user_id,
            article_id=article.id
        )
        return await self.repo.create(comment)

    async def list_comments(self, article: Article) -> list[Comment]:
        return await self.repo.get_by_article(article)

    async def delete_comment(self, comment_id: int, current_user_id: int) -> None:
        comment = await self.repo.get_by_id(comment_id)
        if not comment:
            raise NotFoundException("Комментарий не найден")

        if comment.author_id != current_user_id:
            raise ForbiddenException("Нет доступа для удаления этого комментария")

        await self.repo.delete(comment)
