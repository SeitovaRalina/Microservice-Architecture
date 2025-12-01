from fastapi import Depends, Path

from src.core.di import get_article_service, get_comment_service
from src.services.comment_service import CommentService
from src.services.article_service import ArticleService
from src.schemas.comment import CommentCreate, CommentOut
from backend.src.schemas.profile import ProfileOut
from src.schemas.common import ListResponse, DeleteResponse
from src.core.utils.dependencies import get_current_user_id


async def add_comment(
    payload: CommentCreate,
    slug: str = Path(..., description="Slug статьи"),
    article_service: ArticleService = Depends(get_article_service),
    comment_service: CommentService = Depends(get_comment_service),
    current_user_id: int = Depends(get_current_user_id),
):
    article = await article_service.get_article(slug)
    comment = await comment_service.add_comment(article, current_user_id, payload)

    out = CommentOut.model_validate(comment)
    # out.author = ProfileOut.from_user(current_user)
    out.author = ProfileOut(
        username=f"User {current_user_id}",
    )
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
        # co.author = ProfileOut.from_user(c.author)
        co.author = ProfileOut(
            username=f"User {c.author_id}",
        )
        result.append(co)

    return ListResponse(items=result)


async def delete_comment(
    slug: str = Path(..., description="Slug статьи"),
    comment_id: int = Path(..., description="Уникальный идентификатор комментария"),
    article_service: ArticleService = Depends(get_article_service),
    comment_service: CommentService = Depends(get_comment_service),
    current_user_id: int = Depends(get_current_user_id),
):
    _ = await article_service.get_article(slug)
    await comment_service.delete_comment(comment_id, current_user_id)
    return DeleteResponse(detail="Comment deleted")
