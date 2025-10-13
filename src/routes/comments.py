from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from src.db import get_db
from src.controllers import comments as comments_ctrl
from src.controllers import articles as articles_ctrl
from src.core.utils.dependencies import get_current_user
from src.schemas.comment import CommentCreate, CommentOut
from src.schemas.user import ProfileOut
from src.schemas.common import DeleteResponse, ListResponse

router = APIRouter(prefix="/api/articles/{slug}/comments", tags=["comments"])

@router.post("", response_model=CommentOut, status_code=201,
             summary="Добавить комментарий к статье", description="Добавляет новый комментарий к статье. Требуется аутентификация.")
async def add_comment(payload: CommentCreate,
                      slug: str = Path(..., description="Slug статьи"),
                      db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    article = await articles_ctrl.get_article_by_slug(db, slug)
    comment = await comments_ctrl.add_comment(db, article, current_user, payload)
    out = CommentOut.model_validate(comment)
    out.author = ProfileOut.from_user(current_user)
    return out

@router.get("", response_model=ListResponse[CommentOut],
             summary="Получить комментарии к статье", description="Возвращает список комментариев для указанной статьи.")
async def list_comments(slug: str = Path(..., description="Slug статьи"),
                        db: Session = Depends(get_db)):
    article = await articles_ctrl.get_article_by_slug(db, slug)
    comments = await comments_ctrl.get_comments(db, article)
    out = []
    for c in comments:
        co = CommentOut.model_validate(c)
        co.author = ProfileOut.from_user(c.author)
        out.append(co)
    return out

@router.delete("/{comment_id}", response_model=DeleteResponse,
               summary="Удалить комментарий", description="Удаляет комментарий для указанной статьи по его ID. Требуется аутентификация.")
async def delete_comment(slug: str = Path(..., description="Slug статьи"),
                         comment_id: int = Path(..., description="ID комментария"),
                         db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    _ = await articles_ctrl.get_article_by_slug(db, slug)
    await comments_ctrl.delete_comment(db, comment_id, current_user)
    return {"detail": "Comment deleted"}
