from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_admin_user
from app.models.user import User
from app.models.category import Category
from app.models.tool import Tool
from app.models.file_upload import FileUpload
from app.schemas import Response

router = APIRouter()


@router.get("/stats", response_model=Response)
async def get_stats(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    user_count = (await db.execute(select(func.count()).select_from(User))).scalar() or 0
    category_count = (await db.execute(select(func.count()).select_from(Category))).scalar() or 0
    tool_count = (await db.execute(select(func.count()).select_from(Tool))).scalar() or 0
    file_count = (await db.execute(select(func.count()).select_from(FileUpload))).scalar() or 0
    active_users = (await db.execute(select(func.count()).select_from(User).where(User.is_active))).scalar() or 0
    featured_tools = (await db.execute(select(func.count()).select_from(Tool).where(Tool.is_featured == 1))).scalar() or 0
    return Response.ok(data={
        "users": user_count,
        "active_users": active_users,
        "categories": category_count,
        "tools": tool_count,
        "featured_tools": featured_tools,
        "files": file_count,
    })
