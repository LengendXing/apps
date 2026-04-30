from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, func


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[str] = mapped_column(String(64), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(String(64), server_default=func.now())
