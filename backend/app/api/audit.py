from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_admin_user
from app.models.audit_log import AuditLog
from app.models.user import User
from app.schemas import Response
from app.schemas.common import AuditLogOut

router = APIRouter()


@router.get("/audit-logs", response_model=Response)
async def list_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    action: str = Query(""),
    target_type: str = Query(""),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    q = select(AuditLog)
    if action:
        q = q.where(AuditLog.action == action)
    if target_type:
        q = q.where(AuditLog.target_type == target_type)
    total = (await db.execute(select(func.count()).select_from(q.subquery()))).scalar() or 0
    q = q.order_by(AuditLog.id.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(q)
    logs = result.scalars().all()
    return Response.ok(data={
        "items": [AuditLogOut.model_validate(log).model_dump() for log in logs],
        "total": total, "page": page, "page_size": page_size,
    })
