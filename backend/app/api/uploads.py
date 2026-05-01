import os
import uuid
import json
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.config import get_settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.file_upload import FileUpload
from app.models.audit_log import AuditLog
from app.models.user import User
from app.schemas import Response
from app.schemas.common import FileUploadOut

settings = get_settings()
router = APIRouter()


@router.post("", response_model=Response)
async def upload_file(
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    contents = await file.read()
    if len(contents) > max_size:
        raise HTTPException(status_code=400, detail=f"File too large (max {settings.MAX_FILE_SIZE_MB}MB)")

    ext = os.path.splitext(file.filename or "unknown")[1]
    stored_name = f"{uuid.uuid4().hex}{ext}"
    upload_path = os.path.join(settings.UPLOAD_DIR, stored_name)

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    with open(upload_path, "wb") as f:
        f.write(contents)

    expires_at = (datetime.now(timezone.utc) + timedelta(hours=settings.FILE_EXPIRE_HOURS)).isoformat()
    record = FileUpload(
        original_name=file.filename or "unknown",
        stored_name=stored_name,
        file_size=len(contents),
        content_type=file.content_type or "",
        user_id=user.id,
        expires_at=expires_at,
    )
    db.add(record)
    db.add(AuditLog(user_id=user.id, action="upload", target_type="file", details=json.dumps({"original_name": file.filename})))
    await db.commit()
    await db.refresh(record)

    return Response.ok(data={
        "id": record.id,
        "original_name": record.original_name,
        "url": f"/uploads/{stored_name}",
        "size": len(contents),
        "expires_at": record.expires_at,
    })


@router.get("", response_model=Response)
async def list_uploads(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    q = select(FileUpload).where(FileUpload.user_id == user.id)
    total = (await db.execute(select(func.count()).select_from(q.subquery()))).scalar() or 0
    q = q.order_by(FileUpload.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(q)
    files = result.scalars().all()
    data = [
        {
            "id": f.id, "original_name": f.original_name,
            "url": f"/uploads/{f.stored_name}", "size": f.file_size,
            "content_type": f.content_type, "expires_at": f.expires_at,
        }
        for f in files
    ]
    return Response.ok(data={"items": data, "total": total, "page": page, "page_size": page_size})


@router.delete("/{file_id}", response_model=Response)
async def delete_upload(
    file_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(select(FileUpload).where(FileUpload.id == file_id, FileUpload.user_id == user.id))
    record = result.scalar_one_or_none()
    if record is None:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = os.path.join(settings.UPLOAD_DIR, record.stored_name)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(record)
    db.add(AuditLog(user_id=user.id, action="delete", target_type="file", target_id=file_id))
    await db.commit()
    return Response.ok(data={"deleted": file_id})
