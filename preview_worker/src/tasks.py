import os
import logging
import requests

from src.core.celery_app import celery_app

logger = logging.getLogger(__name__)
BACKEND_URL = os.getenv("BACKEND_SERVICE_URL", "http://backend:8000")
API_KEY = os.getenv("API_KEY_PREVIEW")

@celery_app.task(name="post.generate_preview", bind=True, max_retries=3)
def generate_preview(self, article_id: int, slug: str, title: str, author_id: int):
    try:
        response = requests.get(f"{BACKEND_URL}/api/articles/{slug}")
        response.raise_for_status()

        # Симуляция генерации превью (fake URL)
        preview_url = f"https://fake-preview.com/{slug}.jpg"
        logger.info(f"Generated preview for article {article_id}: {preview_url}")

        # Сохранить превью (internal PUT с ключом)
        headers = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json"
        }
        preview_payload = {"preview_url": preview_url}
        save_response = requests.put(f"{BACKEND_URL}/internal/articles/{slug}/preview", json=preview_payload, headers=headers)
        save_response.raise_for_status()

        # Enqueue следующий шаг
        task_id = f"publish-{article_id}"
        celery_app.send_task(
            'post.publish',
            kwargs={
                'article_id': article_id,
                'slug': slug,
                'title': title,
                'author_id': author_id,
            },
            task_id=task_id,
            queue="publish"
        )

        return {"status": "success", "preview_url": preview_url}

    except Exception as e:
        logger.error(f"Error in post.generate_preview for {article_id}: {e}")

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
