import os
from typing import Literal
import httpx
import logging

logger = logging.getLogger(__name__)

class WebhookService:
    def __init__(self):
        self.backend_service_url = os.getenv(
            "BACKEND_SERVICE_URL", "http://backend:8000"
        )

    async def fire_invalidation(
            self, user_id: int,
            reason: Literal["profile_updated", "account_deleted"] = "profile_updated"
        ) -> None:
        webhook_url = f"{self.backend_service_url}/internal/invalidate-profile-cache"
        payload = {"user_id": user_id, "reason": reason}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {os.getenv('API_KEY_USERS')}",
        }

        try:
            async with httpx.AsyncClient(timeout=1.0) as client:
                await client.post(webhook_url, json=payload, headers=headers)
            logger.info(f"Webhook fired: invalidate profile {user_id} ({reason})")
        except Exception as e:
            logger.error(f"Webhook failed for user {user_id}: {e}")
