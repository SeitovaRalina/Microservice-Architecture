import os
import logging
import requests

from src.core.celery_app import celery_app

logger = logging.getLogger(__name__)
BACKEND_URL = os.getenv("BACKEND_SERVICE_URL", "http://backend:8000")
API_KEY = os.getenv("API_KEY_DLQ")

@celery_app.task(name="compensation.handle_failed_task")
def handle_failed_task(failed_task_name: str, article_id: int, slug: str, error_info: str):
    """
    Компенсация для failed задач из DLQ.
    failed_task_name: "post.moderate", "post.generate_preview", "post.publish", "post.notify"
    """
    try:
        headers = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json"
        }
        logger.info(f"Error info: {error_info}")

        if failed_task_name == "post.moderate":
            # Как будто модерация не прошла
            reject_url = f"{BACKEND_URL}/internal/articles/{slug}/reject"
            response = requests.post(reject_url, headers=headers)
            response.raise_for_status()
            logger.info(f"Compensation: rejected article {article_id} due to moderation failure")

        elif failed_task_name in ["post.generate_preview", "post.publish"]:
            # Техническая ошибка после модерации
            error_url = f"{BACKEND_URL}/internal/articles/{slug}/error"
            response = requests.post(error_url, headers=headers)
            response.raise_for_status()
            logger.info(f"Compensation: marked article {article_id} as ERROR due to {failed_task_name} failure")

        elif failed_task_name == "post.notify":
            # Ничего не компенсируем — пост уже опубликован
            logger.warning(f"No compensation needed for failed notifications on article {article_id}")

        else:
            logger.error(f"Unknown failed task {failed_task_name} for article {article_id}")

    except Exception as e:
        logger.error(f"Compensation failed for article {article_id}: {e}")
