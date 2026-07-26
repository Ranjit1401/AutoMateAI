from datetime import datetime

from pydantic import BaseModel


class MemoryOut(BaseModel):
    id: str
    category: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class MemoryCreate(BaseModel):
    content: str
    category: str = "general"
