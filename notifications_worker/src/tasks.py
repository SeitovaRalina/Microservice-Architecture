import os
import logging
import requests

from src.core.celery_app import celery_app
from src.db import get_db
from src.repositories.subscriber_repository import SubscriberRepository

logger = logging.getLogger(__name__)
PUSH_URL = os.getenv("PUSH_URL")

@celery_app.task(name="post.notify", max_retries=5)
def notify_subscribers(author_id: int, article_id: int, article_title: str):
    title_snippet = article_title[:10] + "..." if len(article_title) > 10 else article_title
    message = f"Пользователь {author_id} выпустил новый пост: {title_snippet}"

    db_gen = get_db()
    db = next(db_gen)

    try:
        repo = SubscriberRepository(db)
        subscribers = repo.get_subscribers_with_keys(author_id)

        if not subscribers:
            logger.info(f"Нет подписчиков для автора {author_id}")
            return

        for sub_id, sub_key in subscribers:
            if not sub_key:
                logger.warning(f"Пропуск: нет ключа у {sub_id}")
                continue

            try:
                response = requests.post(
                    PUSH_URL,
                    json={"message": message},
                    headers={
                        "Authorization": f"Bearer {sub_key}",
                        "Content-Type": "application/json"
                    },
                    timeout=10
                )
                response.raise_for_status()
                logger.info(f"Уведомление отправлено: {sub_id}")
            except requests.RequestException as e:
                logger.error(f"Ошибка отправки {sub_id}: {e}")

        logger.info(f"Обработка уведомлений для статьи {article_id} завершена")
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass
