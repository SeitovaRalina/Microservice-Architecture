from fastapi import APIRouter, Depends

from src.controllers import comments as comments_ctrl
from src.schemas.comment import CommentOut
from src.schemas.common import DeleteResponse, ListResponse


router = APIRouter(prefix="/api/articles/{slug}/comments", tags=["comments"])


@router.post("", response_model=CommentOut, status_code=201,
             summary="Добавить комментарий к статье", description="Добавляет новый комментарий к статье. Требуется аутентификация.")
async def add_comment(payload: CommentOut = Depends(comments_ctrl.add_comment)):
    return payload

@router.get("", response_model=ListResponse[CommentOut],
             summary="Получить комментарии к статье", description="Возвращает список комментариев для указанной статьи.")
async def list_comments(payload: ListResponse[CommentOut] = Depends(comments_ctrl.list_comments)):
    return payload

@router.delete("/{comment_id}", response_model=DeleteResponse,
               summary="Удалить комментарий", description="Удаляет комментарий для указанной статьи по его ID. Требуется аутентификация.")
async def delete_comment(payload: DeleteResponse = Depends(comments_ctrl.delete_comment)):
    return payload
