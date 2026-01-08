from fastapi import APIRouter, Depends

from src.schemas.article import ArticleCreate, ArticleOut, ArticleUpdate
from src.schemas.common import DeleteResponse, PaginatedResponse
from src.controllers import articles as article_ctrl

router = APIRouter(prefix="/api/articles", tags=["articles"])

@router.post("", response_model=ArticleOut, status_code=201,
             summary="Создать статью", description="Создает новую статью. Требуется аутентификация.")
async def create_article(payload: ArticleCreate = Depends(article_ctrl.create_article)):
    return payload

@router.get("", response_model=PaginatedResponse[ArticleOut],
            summary="Получить список статей", description="Возвращает список статей с поддержкой пагинации.")
async def list_articles(payload: PaginatedResponse[ArticleOut] = Depends(article_ctrl.list_articles)):
    return payload

@router.get("/{slug}", response_model=ArticleOut,
             summary="Получить статью по slug", description="Возвращает статью по ее уникальному slug.")
async def get_article(payload: ArticleOut = Depends(article_ctrl.get_article_by_slug)):
    return payload

@router.put("/{slug}", response_model=ArticleOut,
             summary="Обновить статью по slug", description="Обновляет существующую статью по ее slug. Требуется аутентификация.")
async def update_article(payload: ArticleUpdate = Depends(article_ctrl.update_article)):
    return payload

@router.delete("/{slug}", response_model=DeleteResponse,
               summary="Удалить статью по slug", description="Удаляет статью по ее slug. Требуется аутентификация.")
async def delete_article(payload: DeleteResponse = Depends(article_ctrl.delete_article)):
    return payload

@router.post("/{slug}/publish",
             response_model=ArticleOut,
             summary="Запросить публикацию статьи",
             description="Запускает процесс модерации и публикации. Доступно только автору статьи в статусе DRAFT.")
async def request_publish_article(payload: ArticleOut = Depends(article_ctrl.publish_article)):
    return payload