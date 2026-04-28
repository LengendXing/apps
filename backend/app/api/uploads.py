import os
import uuid
import json
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import get_settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.file_upload import FileUpload
from app.models.audit_log import AuditLog
from app.models.user import User
from app.schemas import Response, ERROR_BAD_REQUEST

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

    ext = os.path.splitext(file.filename)[1]
    stored_name = f"{uuid.uuid4().hex}{ext}"
    upload_path = os.path.join(settings.UPLOAD_DIR, stored_name)

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    with open(upload_path, "wb") as f:
        f.write(contents)

    expires_at = datetime.now(timezone.utc) + timedelta(hours=settings.FILE_EXPIRE_HOURS)
    record = FileUpload(
        original_name=file.filename,
        stored_name=stored_name,
        file_size=len(contents),
        content_type=file.content_type,
        user_id=user.id,
        expires_at=expires_at.isoformat(),
    )
    db.add(record)
    db.add(AuditLog(user_id=user.id, action="upload", target_type="file", details=json.dumps({"original_name": file.filename})))
    await db.commit()

    return Response.ok(data={
        "id": record.id,
        "url": f"/uploads/{stored_name}",
        "size": len(contents),
        "expires_at": record.expires_at,
    })


@router.get("", response_model=Response)
async def list_uploads(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(FileUpload).where(FileUpload.user_id == user.id).order_by(FileUpload.created_at.desc())
    )
    files = result.scalars().all()
    return Response.ok(data=[
        {
            "id": f.id,
            "original_name": f.original_name,
            "url": f"/uploads/{f.stored_name}",
            "size": f.file_size,
            "expires_at": f.expires_at,
        }
        for f in files
    ])


@router.delete("/{file_id}", response_model=Response)
async def delete_upload(
    file_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    from app.models.file_upload import FileUpload as FU
    result = await db.execute(select(FU).where(FU.id == file_id, FU.user_id == user.id))
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
