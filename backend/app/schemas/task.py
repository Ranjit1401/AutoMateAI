from datetime import datetime

from pydantic import BaseModel


class TaskOut(BaseModel):
    id: str
    title: str
    agent: str
    action: str
    status: str
    result: dict | None
    error: str | None
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None

    model_config = {"from_attributes": True}
