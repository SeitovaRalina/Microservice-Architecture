from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models.article import Article
from src.models.tag import Tag
from src.models.user import User
from src.schemas import ArticleCreate, ArticleUpdate
from src.utils import make_unique_slug

def article_exists(db: Session, slug: str) -> bool:
    return db.query(Article).filter(Article.slug == slug).first() is not None

def create_article(db: Session, current_user: User, article_in: ArticleCreate) -> Article:
    slug = make_unique_slug(article_in.title, lambda s: article_exists(db, s))
    article = Article(
        title=article_in.title,
        description=article_in.description,
        body=article_in.body,
        slug=slug,
        author=current_user
    )
    # handle tags
    tags_objs = []
    for tag_name in (article_in.tagList or []):
        tag_name_stripped = tag_name.strip().lower()
        tag = db.query(Tag).filter(Tag.name == tag_name_stripped).first()
        if not tag:
            tag = Tag(name=tag_name_stripped)
            db.add(tag)
            db.flush()
        tags_objs.append(tag)
    article.tags = tags_objs
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

def list_articles(db: Session, limit: int = 20, offset: int = 0) -> List[Article]:
    return db.query(Article).order_by(Article.created_at.desc()).offset(offset).limit(limit).all()

def get_article_by_slug(db: Session, slug: str) -> Optional[Article]:
    return db.query(Article).filter(Article.slug == slug).first()

def update_article(db: Session, slug: str, current_user: User, article_in: ArticleUpdate) -> Article:
    article = get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this article")
    if article_in.title:
        article.title = article_in.title
        # potentially update slug — keep same slug for simplicity or regenerate
        article.slug = make_unique_slug(article.title, lambda s: article_exists(db, s) and s != slug)
    if article_in.description:
        article.description = article_in.description
    if article_in.body:
        article.body = article_in.body
    if article_in.tagList is not None:
        article.tags.clear()
        for tag_name in article_in.tagList:
            tn = tag_name.strip().lower()
            tag = db.query(Tag).filter(Tag.name == tn).first()
            if not tag:
                tag = Tag(name=tn)
                db.add(tag)
                db.flush()
            article.tags.append(tag)
    db.commit()
    db.refresh(article)
    return article

def delete_article(db: Session, slug: str, current_user: User):
    article = get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this article")
    db.delete(article)
    db.commit()
    return
