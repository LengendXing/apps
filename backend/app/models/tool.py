from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Tool(Base, TimestampMixin):
    __tablename__ = "ap_tools"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256), index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    url: Mapped[str] = mapped_column(String(2048), default="")
    icon: Mapped[str] = mapped_column(String(512), default="")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("ap_categories.id"), index=True, default=0)
    tags: Mapped[str] = mapped_column(Text, default="[]")
    platforms: Mapped[str] = mapped_column(Text, default="[]")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_featured: Mapped[bool] = mapped_column(default=False)
