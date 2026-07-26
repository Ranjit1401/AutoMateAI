"""Persists application/agent events so the Logs page shows real data
instead of a permanently-empty static array."""
from sqlalchemy.orm import Session

from app.db.models import LogEntry


def add_log(db: Session, message: str, level: str = "info", source: str = "system", user_id: str | None = None, meta: dict | None = None) -> LogEntry:
    entry = LogEntry(user_id=user_id, level=level, source=source, message=message, meta=meta)
    db.add(entry)
    db.flush()
    return entry


def list_logs(db: Session, user_id: str, limit: int = 200) -> list[LogEntry]:
    return (
        db.query(LogEntry)
        .filter((LogEntry.user_id == user_id) | (LogEntry.user_id.is_(None)))
        .order_by(LogEntry.created_at.desc())
        .limit(limit)
        .all()
    )
