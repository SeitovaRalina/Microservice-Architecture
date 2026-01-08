from fastapi import Depends
from fastapi.params import Path, Query

from src.core.di import get_article_service, get_user_cache_service
from src.core.celery_app import celery_app
from src.services.article_service import ArticleService
from src.services.user_cache_service import UserCacheService
from src.schemas.article import ArticleCreate, ArticleUpdate, ArticleOut
from src.schemas.profile import ProfileOut
from src.schemas.common import PaginatedResponse, PaginationMeta, DeleteResponse
from src.core.utils.dependencies import get_current_user_id
from src.models.article import Article


def _to_response(article: Article, profile: ProfileOut) -> ArticleOut:
    resp = ArticleOut.model_validate(article)
    resp.tagList = [tag.name for tag in article.tags]
    resp.author = profile
    return resp


async def create_article(
    data: ArticleCreate,
    user_id: int = Depends(get_current_user_id),
    article_service: ArticleService = Depends(get_article_service),
    cache_service: UserCacheService = Depends(get_user_cache_service)
) -> ArticleOut:
    article = await article_service.create_article(user_id, data)
    profile = await cache_service.get_profile(user_id)

    task_id = f"notify-article-{article.id}-author-{user_id}"
    celery_app.send_task(
        'notify_subscribers',
        kwargs={
            'author_id': user_id,
            'article_id': article.id,
            'article_title': article.title,
        },
        task_id=task_id, # гарантирует идемпотентность
        queue="notifications"
    )

    return _to_response(article, profile)

async def list_articles(
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=100, description="Количество статей на странице"),
    article_service: ArticleService = Depends(get_article_service),
    cache_service: UserCacheService = Depends(get_user_cache_service),
) -> PaginatedResponse[ArticleOut]:
    articles, total, total_pages = await article_service.list_articles(page, per_page)

    items = []
    for a in articles:
        profile = await cache_service.get_profile(a.author_id)
        items.append(_to_response(a, profile))
    meta = PaginationMeta(page=page, per_page=per_page, total_items=total, total_pages=total_pages)
    return PaginatedResponse(items=items, meta=meta)

async def get_article_by_slug(
    slug: str = Path(..., description="Slug статьи"),
    article_service: ArticleService = Depends(get_article_service),
    cache_service: UserCacheService = Depends(get_user_cache_service),
) -> ArticleOut:
    article = await article_service.get_article(slug)
    profile = await cache_service.get_profile(article.author_id)

    return _to_response(article, profile)

async def update_article(
    slug: str = Path(..., description="Slug статьи"),
    data: ArticleUpdate = None,
    user_id: int = Depends(get_current_user_id),
    article_service: ArticleService = Depends(get_article_service),
    cache_service: UserCacheService = Depends(get_user_cache_service),
) -> ArticleOut:
    article = await article_service.update_article(slug, user_id, data)
    profile = await cache_service.get_profile(user_id)

    return _to_response(article, profile)

async def delete_article(
    slug: str = Path(..., description="Slug статьи"),
    user_id: int = Depends(get_current_user_id),
    article_service: ArticleService = Depends(get_article_service),
) -> DeleteResponse:
    await article_service.delete_article(slug, user_id)
    return DeleteResponse(detail="Article deleted")
