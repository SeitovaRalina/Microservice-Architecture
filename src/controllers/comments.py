from fastapi import Depends, Path

from src.core.di import get_article_service, get_comment_service
from src.services.comment_service import CommentService
from src.services.article_service import ArticleService
from src.schemas.comment import CommentCreate, CommentOut
from src.schemas.user import ProfileOut
from src.schemas.common import ListResponse, DeleteResponse
from src.core.utils.dependencies import get_current_user
from src.models.user import User


async def add_comment(
    payload: CommentCreate,
    slug: str = Path(..., description="Slug статьи"),
    article_service: ArticleService = Depends(get_article_service),
    comment_service: CommentService = Depends(get_comment_service),
    current_user: User = Depends(get_current_user),
):
    article = await article_service.get_article(slug)
    comment = await comment_service.add_comment(article, current_user, payload)

    out = CommentOut.model_validate(comment)
    out.author = ProfileOut.from_user(current_user)
    return out


async def list_comments(
    slug: str = Path(..., description="Slug статьи"),
    article_service: ArticleService = Depends(get_article_service),
    comment_service: CommentService = Depends(get_comment_service),
):
    article = await article_service.get_article(slug)
    comments = await comment_service.list_comments(article)

    result = []
    for c in comments:
        co = CommentOut.model_validate(c)
        co.author = ProfileOut.from_user(c.author)
        result.append(co)

    return ListResponse(items=result)


async def delete_comment(
    slug: str = Path(..., description="Slug статьи"),
    comment_id: int = Path(..., description="Уникальный идентификатор комментария"),
    article_service: ArticleService = Depends(get_article_service),
    comment_service: CommentService = Depends(get_comment_service),
    current_user: User = Depends(get_current_user),
):
    _ = await article_service.get_article(slug)
    await comment_service.delete_comment(comment_id, current_user)
    return DeleteResponse(detail="Comment deleted")
