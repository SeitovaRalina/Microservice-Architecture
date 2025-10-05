from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.db import get_db
from src.controllers import comments as comments_ctrl
from src.controllers import articles as articles_ctrl
from src.controllers.auth import get_current_user
from src.schemas import CommentCreate, CommentOut

router = APIRouter()

@router.post("/articles/{slug}/comments", response_model=CommentOut)
def add_comment(slug: str, payload: CommentCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    article = articles_ctrl.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    comment = comments_ctrl.add_comment(db, article, current_user, payload)
    co = CommentOut.model_validate(comment)
    return co

@router.get("/articles/{slug}/comments", response_model=List[CommentOut])
def list_comments(slug: str, db: Session = Depends(get_db)):
    article = articles_ctrl.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    items = comments_ctrl.get_comments(db, article)
    return [CommentOut.model_validate(i) for i in items]

@router.delete("/articles/{slug}/comments/{comment_id}", status_code=204)
def delete_comment(slug: str, comment_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    article = articles_ctrl.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    comments_ctrl.delete_comment(db, comment_id, current_user)
    return {}
