import random
import requests
import os
import logging

from src.core.celery_app import celery_app

logger = logging.getLogger(__name__)
BACKEND_URL = os.getenv("BACKEND_SERVICE_URL", "http://backend:8000")
API_KEY = os.getenv("API_KEY_MODERATION")

@celery_app.task(name="post.moderate", bind=True, max_retries=3)
def moderate_article(self, article_id: int, slug: str, title: str, author_id: int):
    try:
        approved = random.choice([True, False])
        logger.info(f"Moderation for article {article_id}: {'approved' if approved else 'rejected'}")

        if approved:
            # Идемпотентный enqueue следующей задачи
            task_id = f"generate-preview-{article_id}"
            celery_app.send_task(
                'post.generate_preview',
                kwargs={
                    'article_id': article_id,
                    'slug': slug,
                    'title': title,
                    'author_id': author_id
                },
                task_id=task_id,
                queue="preview"
            )
        else:
            # Компенсация: reject с API-ключом
            headers = {
                "Authorization": f"Token {API_KEY}",
                "Content-Type": "application/json"
            }
            reject_url = f"{BACKEND_URL}/internal/articles/{slug}/reject"
            reject_response = requests.post(reject_url, headers=headers)
            reject_response.raise_for_status()
            logger.info(f"Rejected article {article_id}")

        return {"status": "success", "approved": approved}

    except Exception as e:
        logger.error(f"Error in post.moderate for {article_id}: {e}")

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
