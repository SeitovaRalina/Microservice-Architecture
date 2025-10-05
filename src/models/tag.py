from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db import Base
from .association import article_tags
from .article import Article

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)

    articles: Mapped[List["Article"]] = relationship(secondary=article_tags, back_populates="tags")
