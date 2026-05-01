from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=64)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    role: str = "user"

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    role: Optional[str] = Field(None, pattern="^(admin|user)$")


class LoginRequest(BaseModel):
    username: str
    password: str
