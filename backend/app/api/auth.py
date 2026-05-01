from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_admin_user
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas import Response
from app.schemas.auth import UserCreate, LoginRequest, UserOut, UserUpdate

router = APIRouter()


@router.post("/register", response_model=Response)
async def register(body: UserCreate, db: AsyncSession = Depends(get_db), _admin: User = Depends(get_admin_user)):
    existing = await db.execute(select(User).where((User.username == body.username) | (User.email == body.email)))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username or email already exists")
    user = User(username=body.username, email=body.email, password_hash=hash_password(body.password), role="user")
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return Response.ok(data=UserOut.model_validate(user).model_dump())


@router.post("/login", response_model=Response)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == body.username, User.is_active))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return Response.ok(data={"token": token, "user": UserOut.model_validate(user).model_dump()})


@router.get("/me", response_model=Response)
async def me(user: User = Depends(get_current_user)):
    return Response.ok(data=UserOut.model_validate(user).model_dump())
