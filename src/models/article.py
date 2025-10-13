from typing import List, Optional
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base
from src.models.association import article_tags

class Article(Base):
    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str] = mapped_column(String(500))
    body: Mapped[str] = mapped_column(Text)
    slug: Mapped[str] = mapped_column(String(400), unique=True, index=True)

    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    author: Mapped[Optional["User"]] = relationship("User", back_populates="articles", lazy="selectin")

    tags: Mapped[List["Tag"]] = relationship("Tag", secondary=article_tags, back_populates="articles", lazy="selectin")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="article", cascade="all, delete-orphan")
