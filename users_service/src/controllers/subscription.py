from fastapi import Depends
from src.core.utils.dependencies import get_current_user
from src.services.subscription_service import SubscriptionService
from src.services.auth_service import AuthService
from src.schemas.subscription import SubscriptionKeyUpdate, SubscribeRequest, UnsubscribeRequest
from src.schemas.user import UserOut
from src.core.di import get_auth_service, get_subscription_service
from src.models.user import User


async def update_subscription_key(
    payload: SubscriptionKeyUpdate,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserOut:
    """Обновляет subscription_key текущего пользователя"""
    updated_user = await auth_service.set_subscription_key(current_user, payload.subscription_key)
    return UserOut.model_validate(updated_user)


async def subscribe_to_author(
    payload: SubscribeRequest,
    current_user: User = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
) -> None:
    """Подписаться на автора статей"""
    await subscription_service.subscribe_to_author(current_user, payload.target_user_id)
    return None


async def unsubscribe_from_author(
    payload: UnsubscribeRequest,
    current_user: User = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
) -> None:
    """Отписаться от автора"""
    await subscription_service.unsubscribe_from_author(current_user, payload.target_user_id)
    return None
