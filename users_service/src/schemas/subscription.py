from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class SubscriptionKeyUpdate(BaseModel):
    """Схема для обновления subscription_key"""
    subscription_key: Optional[str] = Field(
        None,
        description="Ключ для push-уведомлений (может быть пустым для отключения)",
        example="bb779f9b-44b3-48e7-9576-bbdf7884cbb1"
    )

    model_config = ConfigDict(extra="forbid")

class SubscribeRequest(BaseModel):
    """Схема для подписки на автора"""
    target_user_id: int = Field(..., gt=0, description="ID пользователя, на которого подписываемся")

    model_config = ConfigDict(extra="forbid")

class UnsubscribeRequest(BaseModel):
    """Схема для отписки от автора"""
    target_user_id: int = Field(..., gt=0, description="ID пользователя, от которого отписываемся")

    model_config = ConfigDict(extra="forbid")
