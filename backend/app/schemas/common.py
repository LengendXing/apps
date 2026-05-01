from pydantic import BaseModel, Field
from typing import Optional


class FileUploadOut(BaseModel):
    id: int
    original_name: str
    stored_name: str
    file_size: int
    content_type: str
    user_id: int
    url: str
    expires_at: str

    model_config = {"from_attributes": True}


class AuditLogOut(BaseModel):
    id: int
    user_id: int
    action: str
    target_type: str
    target_id: int
    details: str
    created_at: str

    model_config = {"from_attributes": True}
