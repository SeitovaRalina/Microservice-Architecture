from datetime import datetime
from typing import List, Optional
from sqlalchemy import JSON, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class ApiKey(Base):
    key: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    scopes: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True, default=list)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
