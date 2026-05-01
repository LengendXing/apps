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
from app.schemas import Response
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.schemas.tool import ToolCreate, ToolUpdate, ToolOut

router = APIRouter()


# --- Categories ---

@router.get("/categories", response_model=Response)
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).order_by(Category.sort_order))
    cats = result.scalars().all()
    return Response.ok(data=[CategoryOut.model_validate(c).model_dump() for c in cats])


@router.post("/categories", response_model=Response)
async def create_category(
    body: CategoryCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    existing = await db.execute(select(Category).where(Category.name == body.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Category name already exists")
    cat = Category(name=body.name, icon=body.icon, sort_order=body.sort_order)
    db.add(cat)
    db.add(AuditLog(user_id=user.id, action="create", target_type="category", details=json.dumps({"name": body.name})))
    await db.commit()
    await db.refresh(cat)
    return Response.ok(data=CategoryOut.model_validate(cat).model_dump())


@router.put("/categories/{category_id}", response_model=Response)
async def update_category(
    category_id: int, body: CategoryUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    result = await db.execute(select(Category).where(Category.id == category_id))
    cat = result.scalar_one_or_none()
    if cat is None:
        raise HTTPException(status_code=404, detail="Category not found")
    update_data = body.model_dump(exclude_none=True)
    if "name" in update_data:
        existing = await db.execute(select(Category).where(Category.name == update_data["name"], Category.id != category_id))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Category name already exists")
    for key, value in update_data.items():
        setattr(cat, key, value)
    db.add(AuditLog(user_id=user.id, action="update", target_type="category", target_id=category_id))
    await db.commit()
    await db.refresh(cat)
    return Response.ok(data=CategoryOut.model_validate(cat).model_dump())


@router.delete("/categories/{category_id}", response_model=Response)
async def delete_category(
    category_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    result = await db.execute(select(Category).where(Category.id == category_id))
    cat = result.scalar_one_or_none()
    if cat is None:
        raise HTTPException(status_code=404, detail="Category not found")
    tool_count = (await db.execute(select(func.count()).select_from(Tool).where(Tool.category_id == category_id))).scalar() or 0
    if tool_count > 0:
        raise HTTPException(status_code=400, detail=f"Category has {tool_count} tools, please move or delete them first")
    db.delete(cat)
    db.add(AuditLog(user_id=user.id, action="delete", target_type="category", target_id=category_id))
    await db.commit()
    return Response.ok(data={"deleted": category_id})


# --- Tools ---

def _tool_to_dict(t: Tool) -> dict:
    return {
        "id": t.id, "name": t.name, "description": t.description, "url": t.url,
        "icon": t.icon, "category_id": t.category_id,
        "tags": json.loads(t.tags) if isinstance(t.tags, str) else t.tags or [],
        "platforms": json.loads(t.platforms) if isinstance(t.platforms, str) else t.platforms or [],
        "sort_order": t.sort_order,
        "is_featured": bool(t.is_featured),
    }


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
    return Response.ok(data={"items": [_tool_to_dict(t) for t in tools], "total": total, "page": page, "page_size": page_size})


@router.get("/tools/{tool_id}", response_model=Response)
async def get_tool(tool_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tool).where(Tool.id == tool_id))
    tool = result.scalar_one_or_none()
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return Response.ok(data=_tool_to_dict(tool))


@router.post("/tools", response_model=Response)
async def create_tool(
    body: ToolCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    tool = Tool(
        name=body.name, description=body.description, url=body.url, icon=body.icon,
        category_id=body.category_id,
        tags=json.dumps(body.tags, ensure_ascii=False),
        platforms=json.dumps(body.platforms, ensure_ascii=False),
        sort_order=body.sort_order,
        is_featured=1 if body.is_featured else 0,
    )
    db.add(tool)
    db.add(AuditLog(user_id=user.id, action="create", target_type="tool", details=json.dumps({"name": tool.name})))
    await db.commit()
    await db.refresh(tool)
    return Response.ok(data=_tool_to_dict(tool))


@router.put("/tools/{tool_id}", response_model=Response)
async def update_tool(
    tool_id: int, body: ToolUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    result = await db.execute(select(Tool).where(Tool.id == tool_id))
    tool = result.scalar_one_or_none()
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    update_data = body.model_dump(exclude_none=True)
    if "tags" in update_data and update_data["tags"] is not None:
        update_data["tags"] = json.dumps(update_data["tags"], ensure_ascii=False)
    if "platforms" in update_data and update_data["platforms"] is not None:
        update_data["platforms"] = json.dumps(update_data["platforms"], ensure_ascii=False)
    if "is_featured" in update_data and update_data["is_featured"] is not None:
        update_data["is_featured"] = 1 if update_data["is_featured"] else 0
    for key, value in update_data.items():
        if hasattr(tool, key):
            setattr(tool, key, value)
    db.add(AuditLog(user_id=user.id, action="update", target_type="tool", target_id=tool_id))
    await db.commit()
    await db.refresh(tool)
    return Response.ok(data=_tool_to_dict(tool))


@router.delete("/tools/{tool_id}", response_model=Response)
async def delete_tool(
    tool_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    result = await db.execute(select(Tool).where(Tool.id == tool_id))
    tool = result.scalar_one_or_none()
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    db.delete(tool)
    db.add(AuditLog(user_id=user.id, action="delete", target_type="tool", target_id=tool_id))
    await db.commit()
    return Response.ok(data={"deleted": tool_id})
