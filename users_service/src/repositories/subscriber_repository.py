from sqlalchemy import delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.subscriber import Subscriber


class SubscriberRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def subscribe(self, subscriber_id: int, author_id: int) -> None:
        new_sub = Subscriber(subscriber_id=subscriber_id, author_id=author_id)
        self.session.add(new_sub)
        await self.session.flush([new_sub])

    async def unsubscribe(self, subscriber_id: int, author_id: int) -> int:
        stmt = delete(Subscriber).where(
            and_(
                Subscriber.subscriber_id == subscriber_id,
                Subscriber.author_id == author_id
            )
        )
        result = await self.session.execute(stmt)
        return result.rowcount
