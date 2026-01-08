from fastapi import APIRouter, Depends
from src.core.utils.internal_auth import (
    require_profile_key,
    require_moderation_key,
    require_preview_key,
    require_publish_key,
    require_error_key,
)
from src.schemas.internal import InvalidateCachePayload, SuccessResponse, ApiKeyCreate, ApiKeyResponse
from src.core.utils.dependencies import get_current_user_id
from src.schemas.article import ArticleOut
from src.core.di import get_user_cache_service
from src.controllers import internal as internal_ctrl

router = APIRouter(prefix="/internal", tags=["internal"])


@router.post("/invalidate-profile-cache",
            dependencies=[Depends(require_profile_key)],
            summary="Инвалидировать кэш профиля пользователя",
            description="Инвалидирует кэш профиля пользователя по его user_id. Внутренний эндпоинт.")
async def invalidate_profile_cache(
    payload: InvalidateCachePayload,
    cache_service = Depends(get_user_cache_service)
):
    await cache_service.invalidate(payload.user_id)
    return {"status": "ok", "user_id": payload.user_id, "reason": payload.reason}


@router.post("/articles/{slug}/reject", response_model=SuccessResponse,
             summary="Отклонить статью", description="Отклоняет статью по ее slug. Внутренний эндпоинт.",
             dependencies=[Depends(require_moderation_key)])
async def reject_article(payload: SuccessResponse = Depends(internal_ctrl.internal_reject_article)):
    return payload

@router.post("/articles/{slug}/error", response_model=SuccessResponse,
             summary="Пометить статью как ошибочную", description="Помечает статью как ошибочную по ее slug. Внутренний эндпоинт.",
             dependencies=[Depends(require_error_key)])
async def mark_article_error(payload: SuccessResponse = Depends(internal_ctrl.internal_mark_article_error)):
    return payload

@router.put("/articles/{slug}/preview", response_model=SuccessResponse,
             summary="Сохранить превью статьи", description="Сохраняет превью статьи по ее slug. Внутренний эндпоинт.",
             dependencies=[Depends(require_preview_key)])
async def save_article_preview(payload: SuccessResponse = Depends(internal_ctrl.internal_save_article_preview)):
    return payload

@router.put("/articles/{slug}/publish", response_model=ArticleOut,
             summary="Опубликовать статью", description="Публикует статью по ее slug. Внутренний эндпоинт.",
             dependencies=[Depends(require_publish_key)])
async def publish_article(payload: ArticleOut = Depends(internal_ctrl.internal_publish_article)):
    return payload


@router.post("/api-keys", response_model=ApiKeyResponse,
             summary="Создать внутренний API ключ", description="Создает новый внутренний API ключ. Внутренний эндпоинт.",
             dependencies=[Depends(get_current_user_id)])
async def create_api_key(
        payload: ApiKeyCreate = Depends(internal_ctrl.admin_create_api_key)):
    return payload
