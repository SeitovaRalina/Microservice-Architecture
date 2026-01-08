from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.repositories.subscriber_repository import SubscriberRepository
from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.core.errors.exceptions import NotFoundException, ConflictException, ValidationException


class SubscriptionService:
    def __init__(self, db: AsyncSession):
        self.sub_repo = SubscriberRepository(db)
        self.user_repo = UserRepository(db)

    async def subscribe_to_author(self, subscriber: User, target_user_id: int) -> None:
        if subscriber.id == target_user_id:
            raise ValidationException("Нельзя подписаться на самого себя")

        author = await self.user_repo.get_by_id(target_user_id)
        if not author:
            raise NotFoundException("Пользователь-автор не найден")
        if author.is_deleted:
            raise ValidationException("Нельзя подписаться на удалённого пользователя")

        try:
            await self.sub_repo.subscribe(subscriber.id, target_user_id)
        except IntegrityError:
            raise ConflictException("Вы уже подписаны на этого пользователя")

    async def unsubscribe_from_author(self, subscriber: User, target_user_id: int) -> None:
        rowcount = await self.sub_repo.unsubscribe(subscriber.id, target_user_id)
        if rowcount == 0:
            raise NotFoundException("Подписка не найдена")
