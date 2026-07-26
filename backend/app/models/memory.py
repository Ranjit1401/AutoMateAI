"""Memory ORM model — persistent key facts / preferences per user."""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Memory(Base):
    __tablename__ = "memories"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    # type: "preference" | "fact" | "task_result" | "general"
    type: Mapped[str] = mapped_column(String(50), default="general", nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    # where did this memory come from: "chat" | "settings" | "agent"
    source: Mapped[str] = mapped_column(String(50), default="chat", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Memory id={self.id!r} type={self.type!r}>"
