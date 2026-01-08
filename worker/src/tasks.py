import asyncio
import os
import logging
import httpx
from src.core.celery_app import celery_app
from src.db import get_db
from src.repositories.subscriber_repository import SubscriberRepository

logger = logging.getLogger(__name__)
PUSH_URL = os.getenv("PUSH_URL")

@celery_app.task(name="notify_subscribers", max_retries=5)
def notify_subscribers(author_id: int, article_id: int, article_title: str):
    title_snippet = article_title[:10] + "..." if len(article_title) > 10 else article_title
    message = f"Пользователь {author_id} выпустил новый пост: {title_snippet}"

    asyncio.run(_send_notifications(author_id, message))

    logger.info(f"Задача завершена: article_id={article_id}")

async def _send_notifications(author_id: int, message: str):
    async for session in get_db():
        repo = SubscriberRepository(session)
        subscribers = await repo.get_subscribers_with_keys(author_id)

        if not subscribers:
            logger.info(f"Нет подписчиков для автора {author_id}")
            return

        async with httpx.AsyncClient(timeout=5.0) as client:
            for sub_id, sub_key in subscribers:
                if not sub_key:
                    logger.warning(f"Пропуск: нет ключа у {sub_id}")
                    continue

                try:
                    resp = await client.post(
                        PUSH_URL,
                        json={"message": message},
                        headers={"Authorization": f"Bearer {sub_key}", "Content-Type": "application/json"}
                    )
                    resp.raise_for_status()
                    logger.info(f"Отправлено: {sub_id}")
                except httpx.HTTPError as e:
                    logger.error(f"Ошибка отправки {sub_id}: {e}")
