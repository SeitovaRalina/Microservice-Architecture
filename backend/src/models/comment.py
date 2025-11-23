from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

class Comment(Base):
    body: Mapped[str] = mapped_column(Text)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    author: Mapped["User"] = relationship("User", back_populates="comments")

    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id", ondelete="CASCADE"))
    article: Mapped["Article"] = relationship("Article", back_populates="comments")
