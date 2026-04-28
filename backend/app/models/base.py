from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import func


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at = func.now()
    updated_at = func.now()
