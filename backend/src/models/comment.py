from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

class Comment(Base):
    body: Mapped[str] = mapped_column(Text)

    author_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id", ondelete="CASCADE"))
    article: Mapped["Article"] = relationship("Article", back_populates="comments")
