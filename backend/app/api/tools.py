import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.audit_log import AuditLog
from app.models.category import Category
from app.models.tool import Tool
from app.models.user import User
from app.schemas import Response, ERROR_BAD_REQUEST, ERROR_NOT_FOUND

router = APIRouter()


# --- Categories ---

@router.get("/categories", response_model=Response)
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).order_by(Category.sort_order))
    cats = result.scalars().all()
    return Response.ok(data=[{"id": c.id, "name": c.name, "icon": c.icon, "sort_order": c.sort_order} for c in cats])


@router.post("/categories", response_model=Response)
async def create_category(
    body: dict, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    name = body.get("name", "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="Name required")
    cat = Category(name=name, icon=body.get("icon", ""), sort_order=body.get("sort_order", 0))
    db.add(cat)
    db.add(AuditLog(user_id=user.id, action="create", target_type="category", details=json.dumps({"name": name})))
    await db.commit()
    await db.refresh(cat)
    return Response.ok(data={"id": cat.id, "name": cat.name, "icon": cat.icon})


# --- Tools ---

@router.get("/tools", response_model=Response)
async def list_tools(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str = Query(""),
    category_id: int = Query(0),
    db: AsyncSession = Depends(get_db),
):
    q = select(Tool)
    if search:
        q = q.where((Tool.name.ilike(f"%{search}%")) | (Tool.description.ilike(f"%{search}%")))
    if category_id:
        q = q.where(Tool.category_id == category_id)
    total = (await db.execute(select(func.count()).select_from(q.subquery()))).scalar() or 0
    q = q.order_by(Tool.is_featured.desc(), Tool.sort_order).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(q)
    tools = result.scalars().all()
    data = []
    for t in tools:
        data.append({
            "id": t.id, "name": t.name, "description": t.description, "url": t.url,
            "icon": t.icon, "category_id": t.category_id,
            "tags": json.loads(t.tags) if isinstance(t.tags, str) else [],
            "platforms": json.loads(t.platforms) if isinstance(t.platforms, str) else [],
            "is_featured": t.is_featured,
        })
    return Response.ok(data={"items": data, "total": total, "page": page, "page_size": page_size})


@router.post("/tools", response_model=Response)
async def create_tool(
    body: dict, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    tool = Tool(
        name=body.get("name", ""),
        description=body.get("description", ""),
        url=body.get("url", ""),
        icon=body.get("icon", ""),
        category_id=body.get("category_id", 0),
        tags=json.dumps(body.get("tags", []), ensure_ascii=False),
        platforms=json.dumps(body.get("platforms", []), ensure_ascii=False),
        sort_order=body.get("sort_order", 0),
        is_featured=body.get("is_featured", False),
    )
    db.add(tool)
    db.add(AuditLog(user_id=user.id, action="create", target_type="tool", details=json.dumps({"name": tool.name})))
    await db.commit()
    await db.refresh(tool)
    return Response.ok(data={"id": tool.id, "name": tool.name, "url": tool.url})


@router.put("/tools/{tool_id}", response_model=Response)
async def update_tool(
    tool_id: int, body: dict, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    result = await db.execute(select(Tool).where(Tool.id == tool_id))
    tool = result.scalar_one_or_none()
    if tool is None:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in body.items():
        if key in ("tags", "platforms") and isinstance(value, list):
            setattr(tool, key, json.dumps(value, ensure_ascii=False))
        elif hasattr(tool, key):
            setattr(tool, key, value)
    db.add(AuditLog(user_id=user.id, action="update", target_type="tool", target_id=tool_id))
    await db.commit()
    return Response.ok(data={"id": tool.id, "name": tool.name})


@router.delete("/tools/{tool_id}", response_model=Response)
async def delete_tool(
    tool_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    result = await db.execute(select(Tool).where(Tool.id == tool_id))
    tool = result.scalar_one_or_none()
    if tool is None:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(tool)
    db.add(AuditLog(user_id=user.id, action="delete", target_type="tool", target_id=tool_id))
    await db.commit()
    return Response.ok(data={"deleted": tool_id})
