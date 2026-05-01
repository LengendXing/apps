import os
import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db, async_session
from app.core.dependencies import get_admin_user
from app.core.security import verify_password, hash_password
from app.models.setting import Setting
from app.models.user import User
from app.schemas import Response

router = APIRouter()


@router.get("/settings/access-password")
async def has_access_password(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Setting).where(Setting.key == "access_password"))
    setting = result.scalar_one_or_none()
    return Response.ok(data={"enabled": setting is not None and bool(setting.value)})


@router.post("/settings/access-password/verify")
async def verify_access_password(body: dict, db: AsyncSession = Depends(get_db)):
    password = body.get("password", "")
    result = await db.execute(select(Setting).where(Setting.key == "access_password"))
    setting = result.scalar_one_or_none()
    if setting and verify_password(password, setting.value):
        return Response.ok(data={"verified": True})
    return Response.error(code=401, message="Password incorrect")


@router.put("/settings/access-password")
async def update_access_password(
    body: dict,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    password = body.get("password", "").strip()
    if not password:
        raise HTTPException(status_code=400, detail="Password required")
    hashed = hash_password(password)
    result = await db.execute(select(Setting).where(Setting.key == "access_password"))
    setting = result.scalar_one_or_none()
    if setting:
        setting.value = hashed
    else:
        db.add(Setting(key="access_password", value=hashed, description="C端访问密码"))
    await db.commit()
    return Response.ok(data={"updated": True})


@router.get("/settings/info")
async def get_settings_info(db: AsyncSession = Depends(get_db), _admin: User = Depends(get_admin_user)):
    result = await db.execute(select(Setting))
    settings = result.scalars().all()
    return Response.ok(data=[{"key": s.key, "description": s.description} for s in settings])
