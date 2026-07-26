"""Pydantic schemas for logs and task endpoints."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TaskLogOut(BaseModel):
    id: str
    title: str
    status: str
    task_type: Optional[str]
    agent: Optional[str]
    user_input: Optional[str]
    response: Optional[str]
    duration_ms: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}


class LogsListResponse(BaseModel):
    items: list[TaskLogOut]
    total: int
    page: int
    page_size: int
