from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.schemas.article import ArticleCreate, ArticleOut, ArticleUpdate
from src.schemas.user import ProfileOut
from src.schemas.common import DeleteResponse, PaginatedResponse, PaginationMeta
from src.controllers import articles as articles_ctrl
from src.core.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/articles", tags=["articles"])

@router.post("/articles", response_model=ArticleOut, status_code=201,
             summary="Создать статью", description="Создает новую статью. Требуется аутентификация.")
async def create_article(article_in: ArticleCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    article = await articles_ctrl.create_article(db, current_user, article_in)
    out = ArticleOut.model_validate(article)
    out.tagList = [t.name for t in article.tags]
    out.author = ProfileOut.from_user(current_user)
    return out

@router.get("", response_model=PaginatedResponse[ArticleOut],
            summary="Получить список статей", description="Возвращает список статей с поддержкой пагинации.")
async def list_articles(
        page: int = Query(1, ge=1, description="Номер страницы"),
        per_page: int = Query(10, ge=1, le=100, description="Количество статей на странице"),
        db: AsyncSession = Depends(get_db)
    ):
    articles, total_items, total_pages = await articles_ctrl.list_articles(db, page, per_page)
    out = []
    for a in articles:
        ao = ArticleOut.model_validate(a)
        ao.tagList = [t.name for t in a.tags]
        ao.author = ProfileOut.from_user(a.author)
        out.append(ao)
    meta = PaginationMeta(
        page=page,
        per_page=per_page,
        total_items=total_items,
        total_pages=total_pages
    )
    return PaginatedResponse(items=out, meta=meta)

@router.get("/{slug}", response_model=ArticleOut,
             summary="Получить статью по slug", description="Возвращает статью по ее уникальному slug.")
async def get_article(slug: str = Path(..., description="Slug статьи"),
                      db: AsyncSession = Depends(get_db)):
    article = await articles_ctrl.get_article_by_slug(db, slug)
    ao = ArticleOut.model_validate(article)
    ao.tagList = [t.name for t in article.tags]
    ao.author = ProfileOut.from_user(article.author)
    return ao

@router.put("/{slug}", response_model=ArticleOut,
             summary="Обновить статью по slug", description="Обновляет существующую статью по ее slug. Требуется аутентификация.")
async def update_article(slug: str, article_in: ArticleUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    article = await articles_ctrl.update_article(db, slug, current_user, article_in)
    ao = ArticleOut.model_validate(article)
    ao.tagList = [t.name for t in article.tags]
    ao.author = ProfileOut.from_user(article.author)
    return ao

@router.delete("/{slug}", response_model=DeleteResponse,
               summary="Удалить статью по slug", description="Удаляет статью по ее slug. Требуется аутентификация.")
async def delete_article(slug: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    await articles_ctrl.delete_article(db, slug, current_user)
    return {"detail": "Article deleted"}
