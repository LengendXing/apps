from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_admin_user
from app.core.security import hash_password
from app.models.user import User
from app.schemas import Response
from app.schemas.auth import UserOut, UserUpdate

router = APIRouter()


@router.get("/users", response_model=Response)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    q = select(User).order_by(User.id)
    total = (await db.execute(select(func.count()).select_from(q.subquery()))).scalar() or 0
    q = q.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(q)
    users = result.scalars().all()
    return Response.ok(data={
        "items": [UserOut.model_validate(u).model_dump() for u in users],
        "total": total, "page": page, "page_size": page_size,
    })


@router.put("/users/{user_id}", response_model=Response)
async def update_user(
    user_id: int,
    body: UserUpdate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = body.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return Response.ok(data=UserOut.model_validate(user).model_dump())


@router.delete("/users/{user_id}", response_model=Response)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    if user_id == _admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    await db.commit()
    return Response.ok(data={"deleted": user_id})
