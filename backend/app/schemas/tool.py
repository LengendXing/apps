from pydantic import BaseModel, Field
from typing import Optional


class ToolCreate(BaseModel):
    name: str = Field(min_length=1, max_length=256)
    description: str = Field(default="", max_length=2000)
    url: str = Field(default="", max_length=2048)
    icon: str = Field(default="", max_length=512)
    category_id: int = Field(default=0, ge=0)
    tags: list[str] = Field(default_factory=list)
    platforms: list[str] = Field(default_factory=list)
    sort_order: int = Field(default=0, ge=0)
    is_featured: bool = Field(default=False)


class ToolUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=256)
    description: Optional[str] = Field(None, max_length=2000)
    url: Optional[str] = Field(None, max_length=2048)
    icon: Optional[str] = Field(None, max_length=512)
    category_id: Optional[int] = Field(None, ge=0)
    tags: Optional[list[str]] = None
    platforms: Optional[list[str]] = None
    sort_order: Optional[int] = Field(None, ge=0)
    is_featured: Optional[bool] = None


class ToolOut(BaseModel):
    id: int
    name: str
    description: str
    url: str
    icon: str
    category_id: int
    tags: list[str]
    platforms: list[str]
    sort_order: int
    is_featured: bool

    model_config = {"from_attributes": True}
