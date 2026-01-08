import os
import logging
import requests

from src.core.celery_app import celery_app

logger = logging.getLogger(__name__)
BACKEND_URL = os.getenv("BACKEND_SERVICE_URL", "http://backend:8000")
API_KEY = os.getenv("API_KEY_PUBLISH")

@celery_app.task(name="post.publish", bind=True, max_retries=3)
def publish_article(self, article_id: int, slug: str, title: str, author_id: int):
    try:
        # Публикация (internal PUT с ключом)
        headers = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json"
        }
        publish_url = f"{BACKEND_URL}/internal/articles/{slug}/publish"
        publish_response = requests.put(publish_url, headers=headers)
        publish_response.raise_for_status()
        logger.info(f"Published article {article_id}")

        # Enqueue уведомления (post.notify)
        task_id = f"notify-article-{article_id}"
        celery_app.send_task(
            'post.notify',
            kwargs={
                'author_id': author_id,
                'article_id': article_id,
                'article_title': title,
            },
            task_id=task_id,
            queue="notifications"
        )

        return {"status": "success"}

    except Exception as e:
        logger.error(f"Error in post.publish for {article_id}: {e}")

        if self.request.retries >= self.max_retries:
            # Отправляем в DLQ
            celery_app.send_task(
                "compensation.handle_failed_task",
                kwargs={
                    "failed_task_name": self.name,
                    "article_id": article_id,
                    "slug": slug,
                    "error_info": str(e)
                },
                queue="dlq"
            )
            logger.info(f"Task {self.name} for {article_id} moved to DLQ")

        raise self.retry(exc=e, countdown=2 ** self.request.retries)
