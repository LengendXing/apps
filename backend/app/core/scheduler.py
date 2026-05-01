import os
import json
from datetime import datetime, timezone

from sqlalchemy import select, delete
from app.core.config import get_settings
from app.core.database import async_session
from app.models.file_upload import FileUpload

settings = get_settings()


async def cleanup_expired_files():
    now = datetime.now(timezone.utc).isoformat()
    async with async_session() as db:
        result = await db.execute(select(FileUpload).where(FileUpload.expires_at < now))
        expired = result.scalars().all()
        for f in expired:
            file_path = os.path.join(settings.UPLOAD_DIR, f.stored_name)
            if os.path.exists(file_path):
                os.remove(file_path)
            db.delete(f)
        if expired:
            await db.commit()
