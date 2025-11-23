from fastapi import Depends
from fastapi.params import Path, Query

from src.core.di import get_article_service
from src.services.article_service import ArticleService
from src.schemas.article import ArticleCreate, ArticleUpdate, ArticleOut
from src.schemas.user import ProfileOut
from src.schemas.common import PaginatedResponse, PaginationMeta, DeleteResponse
from src.core.utils.dependencies import get_current_user
from src.models.user import User
from src.models.article import Article


def _to_response(article: Article, author: User) -> ArticleOut:
    resp = ArticleOut.model_validate(article)
    resp.tagList = [tag.name for tag in article.tags]
    resp.author = ProfileOut.from_user(author)
    return resp


async def create_article(
    data: ArticleCreate,
    service: ArticleService = Depends(get_article_service),
    user: User = Depends(get_current_user),
) -> ArticleOut:
    article = await service.create_article(user, data)
    return _to_response(article, user)

async def list_articles(
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=100, description="Количество статей на странице"),
    service: ArticleService = Depends(get_article_service),
) -> PaginatedResponse[ArticleOut]:
    articles, total, total_pages = await service.list_articles(page, per_page)
    items = [_to_response(a, a.author) for a in articles]
    meta = PaginationMeta(page=page, per_page=per_page, total_items=total, total_pages=total_pages)
    return PaginatedResponse(items=items, meta=meta)

async def get_article_by_slug(
    slug: str = Path(..., description="Slug статьи"),
    service: ArticleService = Depends(get_article_service),
) -> ArticleOut:
    article = await service.get_article(slug)
    return _to_response(article, article.author)

async def update_article(
    slug: str = Path(..., description="Slug статьи"),
    data: ArticleUpdate = None,
    service: ArticleService = Depends(get_article_service),
    user: User = Depends(get_current_user),
) -> ArticleOut:
    article = await service.update_article(slug, user, data)
    return _to_response(article, article.author)

async def delete_article(
    slug: str = Path(..., description="Slug статьи"),
    service: ArticleService = Depends(get_article_service),
    user: User = Depends(get_current_user),
) -> DeleteResponse:
    await service.delete_article(slug, user)
    return DeleteResponse(detail="Article deleted")
