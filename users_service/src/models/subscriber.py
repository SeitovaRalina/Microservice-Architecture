from sqlalchemy import ForeignKey, UniqueConstraint
from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column

class Subscriber(Base):
    subscriber_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("subscriber_id", "author_id", name="ux_sub"),
    )
