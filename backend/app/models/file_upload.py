from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class FileUpload(Base, TimestampMixin):
    __tablename__ = "ap_file_uploads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    original_name: Mapped[str] = mapped_column(String(512))
    stored_name: Mapped[str] = mapped_column(String(512))
    file_size: Mapped[int] = mapped_column(Integer, default=0)
    content_type: Mapped[str] = mapped_column(String(128), default="")
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    expires_at: Mapped[str] = mapped_column(String(64), default="")
