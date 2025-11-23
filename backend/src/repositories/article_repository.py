from typing import List, Optional, Sequence
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.article import Article
from src.models.tag import Tag


class ArticleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_slug(self, slug: str) -> Optional[Article]:
        result = await self.session.execute(select(Article).where(Article.slug == slug))
        return result.scalar_one_or_none()

    async def create(self, article: Article) -> Article:
        self.session.add(article)
        await self.session.flush([article])
        return article

    async def update(self, article: Article) -> None:
        await self.session.flush([article])
        await self.session.refresh(article)

    async def delete(self, article: Article) -> None:
        await self.session.delete(article)

    async def list_paginated(
        self,
        page: int,
        per_page: int
    ) -> tuple[Sequence[Article], int]:
        offset = (page - 1) * per_page

        result = await self.session.execute(
            select(Article)
            .order_by(Article.created_at.desc())
            .offset(offset)
            .limit(per_page)
        )
        articles = result.scalars().all()

        total = await self.session.scalar(select(func.count(Article.id)))
        return articles, total or 0

    async def slug_exists(self, slug: str, exclude_slug: Optional[str] = None) -> bool:
        query = select(Article.id).where(Article.slug == slug)
        if exclude_slug:
            query = query.where(Article.slug != exclude_slug)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def get_or_create_tags(self, tag_names: List[str]) -> List[Tag]:
        if not tag_names:
            return []

        normalized = [name.strip().lower() for name in tag_names if name.strip()]
        if not normalized:
            return []

        result = await self.session.execute(
            select(Tag).where(Tag.name.in_(normalized))
        )
        existing = {tag.name: tag for tag in result.scalars().all()}

        missing = [name for name in normalized if name not in existing]
        if missing:
            new_tags = [Tag(name=name) for name in missing]
            self.session.add_all(new_tags)
            await self.session.flush(new_tags)
            for tag in new_tags:
                existing[tag.name] = tag

        return [existing[name] for name in normalized]
