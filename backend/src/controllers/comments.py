from fastapi import Depends, Path

from src.core.di import get_article_service, get_comment_service, get_user_cache_service
from src.services.comment_service import CommentService
from src.services.article_service import ArticleService
from src.services.user_cache_service import UserCacheService
from src.schemas.comment import CommentCreate, CommentOut
from src.schemas.profile import ProfileOut
from src.schemas.common import ListResponse, DeleteResponse
from src.core.utils.dependencies import get_current_user_id


async def add_comment(
    payload: CommentCreate,
    slug: str = Path(..., description="Slug статьи"),
    article_service: ArticleService = Depends(get_article_service),
    comment_service: CommentService = Depends(get_comment_service),
    cache_service: UserCacheService = Depends(get_user_cache_service),
    current_user_id: int = Depends(get_current_user_id),
):
    article = await article_service.get_article(slug)
    comment = await comment_service.add_comment(article, current_user_id, payload)
    profile = await cache_service.get_profile(current_user_id)

    out = CommentOut.model_validate(comment)
    out.author = profile
    return out


async def list_comments(
    slug: str = Path(..., description="Slug статьи"),
    article_service: ArticleService = Depends(get_article_service),
    comment_service: CommentService = Depends(get_comment_service),
    cache_service: UserCacheService = Depends(get_user_cache_service)
):
    article = await article_service.get_article(slug)
    comments = await comment_service.list_comments(article)

    result = []
    for c in comments:
        profile = await cache_service.get_profile(c.author_id)
        co = CommentOut.model_validate(c)
        co.author = profile
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
