from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.db import get_db
from src.schemas import ArticleCreate, ArticleOut, ArticleUpdate
from src.controllers import articles as articles_ctrl
from src.controllers.auth import get_current_user

router = APIRouter()

@router.post("/articles", response_model=ArticleOut)
def create_article(article_in: ArticleCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    article = articles_ctrl.create_article(db, current_user, article_in)
    out = ArticleOut.model_validate(article)
    out.tagList = [t.name for t in article.tags]
    return out

@router.get("/articles", response_model=List[ArticleOut])
def list_articles(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    articles = articles_ctrl.list_articles(db, limit=limit, offset=offset)
    out = []
    for a in articles:
        ao = ArticleOut.model_validate(a)
        ao.tagList = [t.name for t in a.tags]
        out.append(ao)
    return out

@router.get("/articles/{slug}", response_model=ArticleOut)
def get_article(slug: str, db: Session = Depends(get_db)):
    article = articles_ctrl.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    ao = ArticleOut.model_validate(article)
    ao.tagList = [t.name for t in article.tags]
    return ao

@router.put("/articles/{slug}", response_model=ArticleOut)
def update_article(slug: str, article_in: ArticleUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    article = articles_ctrl.update_article(db, slug, current_user, article_in)
    ao = ArticleOut.model_validate(article)
    ao.tagList = [t.name for t in article.tags]
    return ao

@router.delete("/articles/{slug}", status_code=204)
def delete_article(slug: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    articles_ctrl.delete_article(db, slug, current_user)
    return {}
