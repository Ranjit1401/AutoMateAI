"""Pydantic schemas for the memory API."""
from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel


class MemoryCreate(BaseModel):
    content: str
    type: Literal["preference", "fact", "task_result", "general"] = "general"
    source: str = "manual"


class MemoryUpdate(BaseModel):
    content: Optional[str] = None
    type: Optional[Literal["preference", "fact", "task_result", "general"]] = None


class MemoryOut(BaseModel):
    id: str
    type: str
    content: str
    source: str
    created_at: datetime

    model_config = {"from_attributes": True}
