from pydantic import BaseModel, Field
from typing import Optional


class AuditLogOut(BaseModel):
    id: int
    user_id: int
    action: str
    target_type: str
    target_id: int
    details: str
    created_at: str

    model_config = {"from_attributes": True}
