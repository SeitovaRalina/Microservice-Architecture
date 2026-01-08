from sqlalchemy.ext.asyncio import AsyncSession

from src.models.article import Article
from src.schemas.article import ArticleCreate, ArticleUpdate
from src.repositories.article_repository import ArticleRepository
from src.core.utils.slug import make_unique_slug
from src.core.errors.exceptions import NotFoundException, ForbiddenException, ConflictException


class ArticleService:
    def __init__(self, db: AsyncSession):
        self.repo = ArticleRepository(db)

    async def create_article(self, current_user_id: int, data: ArticleCreate) -> Article:
        slug = await make_unique_slug(data.title, self.repo.slug_exists)

        article = Article(
            title=data.title,
            description=data.description,
            body=data.body,
            slug=slug,
            author_id=current_user_id,
        )

        tags = await self.repo.get_or_create_tags(data.tagList or [])
        article.tags.extend(tags)

        return await self.repo.create(article)

    async def get_article(self, slug: str) -> Article:
        article = await self.repo.get_by_slug(slug)
        if not article:
            raise NotFoundException("Статья не найдена")
        return article

    async def list_articles(self, page: int, per_page: int):
        articles, total = await self.repo.list_paginated(page, per_page)
        total_pages = (total + per_page - 1) // per_page if total else 1
        return articles, total, total_pages

    async def update_article(self, slug: str, current_user_id: int, data: ArticleUpdate) -> Article:
        article = await self.get_article(slug)

        if article.author_id != current_user_id:
            raise ForbiddenException("Нет доступа для редактирования этой статьи")

        update_data = data.model_dump(exclude_unset=True)

        if "title" in update_data:
            async def exists_check(s: str) -> bool:
                return await self.repo.slug_exists(s, exclude_slug=slug)
            article.slug = await make_unique_slug(update_data["title"], exists_check)

        for field in ("title", "description", "body"):
            if field in update_data:
                setattr(article, field, update_data[field])

        if "tagList" in update_data:
            article.tags.clear()
            if update_data["tagList"]:
                tags = await self.repo.get_or_create_tags(update_data["tagList"])
                article.tags.extend(tags)

        await self.repo.update(article)
        return article

    async def delete_article(self, slug: str, current_user_id: int) -> None:
        article = await self.get_article(slug)
        if article.author_id != current_user_id:
            raise ForbiddenException("Нет доступа для удаления этой статьи")
        await self.repo.delete(article)

    async def update_article_status(self, article: Article, new_status: str) -> Article:
        article.status = new_status
        await self.repo.update(article)
        return article

    async def set_article_preview(self, slug: str, preview_url: str) -> Article:
        article = await self.get_article(slug)
        if article.preview_url == preview_url:
            return article
        article.preview_url = preview_url
        await self.repo.update(article)
        return article

    async def reject_article(self, slug: str) -> Article:
        article = await self.get_article(slug)
        if article.status not in {"DRAFT", "PENDING_PUBLISH"}:
            raise ConflictException("Cannot reject article in current state")
        return await self.update_article_status(article, "REJECTED")

    async def mark_article_error(self, slug: str) -> Article:
        article = await self.get_article(slug)
        return await self.update_article_status(article, "ERROR")

    async def publish_article(self, slug: str) -> Article:
        article = await self.get_article(slug)
        if article.status != "PENDING_PUBLISH":
            raise ConflictException("Article is not pending publish")
        article = await self.update_article_status(article, "PUBLISHED")
        return article

    async def request_article_publication(self, slug: str, current_user_id: int) -> Article:
        article = await self.get_article(slug)

        if article.author_id != current_user_id:
            raise ForbiddenException("Нет доступа для публикации этой статьи")
        if article.status != "DRAFT":
            raise ConflictException(f"Нельзя опубликовать статью в статусе {article.status}")

        article = await self.update_article_status(article, "PENDING_PUBLISH")
        return article
