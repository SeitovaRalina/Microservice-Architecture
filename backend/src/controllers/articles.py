from fastapi import Depends
from fastapi.params import Path, Query

from src.core.di import get_article_service
from src.services.article_service import ArticleService
from src.schemas.article import ArticleCreate, ArticleUpdate, ArticleOut
from backend.src.schemas.profile import ProfileOut
from src.schemas.common import PaginatedResponse, PaginationMeta, DeleteResponse
from src.core.utils.dependencies import get_current_user_id
from src.models.article import Article


def _to_response(article: Article, author_id: int) -> ArticleOut:
    resp = ArticleOut.model_validate(article)
    resp.tagList = [tag.name for tag in article.tags]
    # resp.author = ProfileOut.from_user(author)
    resp.author = ProfileOut(
        username=f"User {author_id}",
    )
    return resp


async def create_article(
    data: ArticleCreate,
    service: ArticleService = Depends(get_article_service),
    user_id: int = Depends(get_current_user_id),
) -> ArticleOut:
    article = await service.create_article(user_id, data)
    return _to_response(article, user_id)

async def list_articles(
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=100, description="Количество статей на странице"),
    service: ArticleService = Depends(get_article_service),
) -> PaginatedResponse[ArticleOut]:
    articles, total, total_pages = await service.list_articles(page, per_page)
    items = [_to_response(a, a.author_id) for a in articles]
    meta = PaginationMeta(page=page, per_page=per_page, total_items=total, total_pages=total_pages)
    return PaginatedResponse(items=items, meta=meta)

async def get_article_by_slug(
    slug: str = Path(..., description="Slug статьи"),
    service: ArticleService = Depends(get_article_service),
) -> ArticleOut:
    article = await service.get_article(slug)
    return _to_response(article, article.author_id)

async def update_article(
    slug: str = Path(..., description="Slug статьи"),
    data: ArticleUpdate = None,
    service: ArticleService = Depends(get_article_service),
    user_id: int = Depends(get_current_user_id),
) -> ArticleOut:
    article = await service.update_article(slug, user_id, data)
    return _to_response(article, article.author_id)

async def delete_article(
    slug: str = Path(..., description="Slug статьи"),
    service: ArticleService = Depends(get_article_service),
    user_id: int = Depends(get_current_user_id),
) -> DeleteResponse:
    await service.delete_article(slug, user_id)
    return DeleteResponse(detail="Article deleted")
