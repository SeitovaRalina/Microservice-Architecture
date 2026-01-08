from sqlalchemy import select, and_

from src.models.subscriber import Subscriber
from src.models.user import User


class SubscriberRepository:
    def __init__(self, session):
        self.session = session

    def get_subscribers_with_keys(self, author_id: int) -> list[tuple[int, str | None]]:
        stmt = select(User.id, User.subscription_key).join(
            Subscriber, Subscriber.subscriber_id == User.id
        ).where(
            and_(
                Subscriber.author_id == author_id,
                User.is_deleted == False  # Пропускаем удалённых
            )
        )
        result = self.session.execute(stmt)
        return result.all()
