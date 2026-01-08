from fastapi import Depends
from fastapi.params import Path

from src.core.errors.exceptions import ForbiddenException
from src.core.utils.dependencies import get_current_user_id
from src.core.di import get_api_key_service, get_article_service, get_user_cache_service
from src.services.article_service import ArticleService
from src.services.user_cache_service import UserCacheService
from src.schemas.article import ArticleOut
from src.schemas.profile import ProfileOut
from src.schemas.internal import ApiKeyCreate, ApiKeyResponse, SuccessResponse, ArticlePreviewCreate
from src.models.article import Article

def _to_response(article: Article, profile: ProfileOut) -> ArticleOut:
    resp = ArticleOut.model_validate(article)
    resp.tagList = [tag.name for tag in article.tags]
    resp.author = profile
    return resp

async def internal_reject_article(
    slug: str = Path(..., description="Уникальный slug статьи"),
    article_service: ArticleService = Depends(get_article_service),
) -> SuccessResponse:
    await article_service.reject_article(slug)
    return SuccessResponse(detail="Article rejected")

async def internal_mark_article_error(
    slug: str = Path(..., description="Уникальный slug статьи"),
    article_service: ArticleService = Depends(get_article_service),
) -> SuccessResponse:
    await article_service.mark_article_error(slug)
    return SuccessResponse(detail="Article marked as error")

async def internal_save_article_preview(
    slug: str = Path(..., description="Уникальный slug статьи"),
    preview_data: ArticlePreviewCreate = ...,
    article_service: ArticleService = Depends(get_article_service),
) -> SuccessResponse:
    await article_service.set_article_preview(slug, preview_data.preview_url)
    return SuccessResponse(detail="Article preview saved")

async def internal_publish_article(
    slug: str = Path(..., description="Уникальный slug статьи"),
    article_service: ArticleService = Depends(get_article_service),
    cache_service: UserCacheService = Depends(get_user_cache_service),
) -> ArticleOut:
    article = await article_service.publish_article(slug)
    profile = await cache_service.get_profile(article.author_id)
    return _to_response(article, profile)


async def admin_create_api_key(
    payload: ApiKeyCreate,
    user_id: int = Depends(get_current_user_id),
    api_key_service = Depends(get_api_key_service),
) -> ApiKeyResponse:
    if user_id != 1:
        raise ForbiddenException("Недостаточно прав.")
    api_key = await api_key_service.generate_key(payload)
    return ApiKeyResponse(
        id=api_key.id,
        key=api_key.key,
        description=api_key.description,
        scopes=api_key.scopes,
        expires_at=api_key.expires_at,
    )
