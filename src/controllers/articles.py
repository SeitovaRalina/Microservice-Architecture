from typing import List, Optional, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.article import Article
from src.models.tag import Tag
from src.models.user import User
from src.schemas.article import ArticleCreate, ArticleUpdate
from src.core.utils.slug import make_unique_slug
from src.core.errors.exceptions import NotFoundException, ForbiddenException

async def article_exists(db: AsyncSession, slug: str) -> bool:
    q = await db.execute(select(Article).where(Article.slug == slug))
    return q.scalar_one_or_none() is not None

async def create_article(db: AsyncSession, current_user: User, article_in: ArticleCreate) -> Article:
    async def exists_check(s):
        return await article_exists(db, s)
    slug = await make_unique_slug(article_in.title, exists_check)
    article = Article(
        title=article_in.title,
        description=article_in.description,
        body=article_in.body,
        slug=slug,
        author_id=current_user.id
    )
    tags_objs = []
    if article_in.tagList:
        for tag_name in article_in.tagList:
            tag_name_stripped = tag_name.strip().lower()
            q = await db.execute(select(Tag).where(Tag.name == tag_name_stripped))
            tag = q.scalar_one_or_none()
            if not tag:
                tag = Tag(name=tag_name_stripped)
                db.add(tag)
                await db.flush()
            tags_objs.append(tag)
    article.tags = tags_objs

    db.add(article)
    await db.commit()
    await db.refresh(article)
    return article

async def list_articles(db: AsyncSession, page: int = 1, per_page: int = 10) -> Tuple[List[Article], int, int]:
    offset = (page - 1) * per_page
    q = await db.execute(
        select(Article)
        .offset(offset)
        .limit(per_page)
    )
    articles = q.scalars().all()

    total_items = await db.scalar(select(func.count(Article.id)))
    total_pages = (total_items + per_page - 1) // per_page if total_items > 0 else 1

    return articles, total_items, total_pages

async def get_article_by_slug(db: AsyncSession, slug: str) -> Optional[Article]:
    q = await db.execute(select(Article).where(Article.slug == slug))
    article = q.scalar_one_or_none()

    if not article:
        raise NotFoundException("Статья не найдена")
    return article

async def update_article(db: AsyncSession, slug: str, current_user: User, article_in: ArticleUpdate) -> Article:
    article = await get_article_by_slug(db, slug)

    if article.author_id != current_user.id:
        raise ForbiddenException(status_code=403, detail="Нет доступа для редактирования этой статьи")

    if article_in.title:
        article.title = article_in.title
        async def exists_check(s):
            found = await article_exists(db, s)
            return found and s != slug
        article.slug = await make_unique_slug(article.title, exists_check)
    if article_in.description:
        article.description = article_in.description
    if article_in.body:
        article.body = article_in.body
    if article_in.tagList is not None:
        article.tags.clear()
        for tag_name in article_in.tagList:
            tn = tag_name.strip().lower()
            q = await db.execute(select(Tag).where(Tag.name == tn))
            tag = q.scalar_one_or_none()
            if not tag:
                tag = Tag(name=tn)
                db.add(tag)
                await db.flush()
            article.tags.append(tag)

    await db.commit()
    await db.refresh(article)

    return article

async def delete_article(db: AsyncSession, slug: str, current_user: User):
    article = await get_article_by_slug(db, slug)

    if article.author_id != current_user.id:
        raise ForbiddenException(status_code=403, detail="Нет доступа для удаления этой статьи")

    await db.delete(article)
    await db.commit()
