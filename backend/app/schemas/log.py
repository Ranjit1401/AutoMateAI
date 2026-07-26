from datetime import datetime

from pydantic import BaseModel


class LogOut(BaseModel):
    id: str
    level: str
    source: str
    message: str
    meta: dict | None
    created_at: datetime

    model_config = {"from_attributes": True}
