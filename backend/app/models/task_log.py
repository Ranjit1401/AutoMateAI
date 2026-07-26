"""TaskLog ORM model — records every agent pipeline execution."""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TaskLog(Base):
    __tablename__ = "task_logs"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    # Optional — null means anonymous / unauthenticated user
    user_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=True, index=True
    )
    session_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    # First 100 chars of the user's message
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    # "running" | "completed" | "failed"
    status: Mapped[str] = mapped_column(String(20), default="completed", nullable=False)
    # "travel" | "coding" | "general" etc.
    task_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    # Which agent handled the final step
    agent: Mapped[str | None] = mapped_column(String(100), nullable=True)
    user_input: Mapped[str | None] = mapped_column(Text, nullable=True)
    response: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<TaskLog id={self.id!r} status={self.status!r}>"
