from datetime import datetime

from sqlalchemy import func, text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ShortLink(Base):
    slug: Mapped[str] = mapped_column(primary_key=True, index=True)
    url: Mapped[str] = mapped_column(nullable=False)
    clicks: Mapped[int] = mapped_column(server_default=text("0"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
