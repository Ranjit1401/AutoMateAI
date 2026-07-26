"""DB-backed long-term memory: stores durable facts extracted from
conversations (see app/agents/memory_agent.py) and retrieves them so future
turns can actually use them (closing the loop the audit flagged as broken)."""
from sqlalchemy.orm import Session

from app.db.models import MemoryEntry


def add_memory(db: Session, user_id: str, content: str, category: str = "general", source_conversation_id: str | None = None) -> MemoryEntry:
    entry = MemoryEntry(user_id=user_id, content=content, category=category, source_conversation_id=source_conversation_id)
    db.add(entry)
    db.flush()
    return entry


def list_memories(db: Session, user_id: str) -> list[MemoryEntry]:
    return (
        db.query(MemoryEntry)
        .filter(MemoryEntry.user_id == user_id)
        .order_by(MemoryEntry.created_at.desc())
        .all()
    )


def recent_memory_strings(db: Session, user_id: str, limit: int = 15) -> list[str]:
    entries = (
        db.query(MemoryEntry)
        .filter(MemoryEntry.user_id == user_id)
        .order_by(MemoryEntry.created_at.desc())
        .limit(limit)
        .all()
    )
    return [e.content for e in entries]


def delete_memory(db: Session, user_id: str, memory_id: str) -> bool:
    entry = db.get(MemoryEntry, memory_id)
    if entry is None or entry.user_id != user_id:
        return False
    db.delete(entry)
    return True
