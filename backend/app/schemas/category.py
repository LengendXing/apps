from pydantic import BaseModel, Field
from typing import Optional


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    icon: str = Field(default="", max_length=64)
    sort_order: int = Field(default=0, ge=0)


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=128)
    icon: Optional[str] = Field(None, max_length=64)
    sort_order: Optional[int] = Field(None, ge=0)


class CategoryOut(BaseModel):
    id: int
    name: str
    icon: str
    sort_order: int

    model_config = {"from_attributes": True}
