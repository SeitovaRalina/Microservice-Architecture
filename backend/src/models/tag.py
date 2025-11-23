from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base
from .association import article_tags

class Tag(Base):
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    articles: Mapped[List["Article"]] = relationship("Article", secondary=article_tags, back_populates="tags")
