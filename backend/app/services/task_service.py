"""Persisted task queue backing the Tasks page and the agent pipeline's
work units. Each chat request that runs the agent graph is recorded as a
Task with a lifecycle (pending -> running -> done|failed), which is the
Task Scheduler / Task Queue the audit flagged as entirely absent."""
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models import Task


def create_task(db: Session, user_id: str, title: str, agent: str, action: str, conversation_id: str | None = None) -> Task:
    task = Task(user_id=user_id, conversation_id=conversation_id, title=title, agent=agent, action=action, status="pending")
    db.add(task)
    db.flush()
    return task


def mark_running(db: Session, task: Task) -> None:
    task.status = "running"
    task.started_at = datetime.now(timezone.utc)
    db.flush()


def mark_done(db: Session, task: Task, result: dict) -> None:
    task.status = "done"
    task.result = result
    task.finished_at = datetime.now(timezone.utc)
    db.flush()


def mark_failed(db: Session, task: Task, error: str) -> None:
    task.status = "failed"
    task.error = error
    task.finished_at = datetime.now(timezone.utc)
    db.flush()


def list_tasks(db: Session, user_id: str, limit: int = 100) -> list[Task]:
    return (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
        .limit(limit)
        .all()
    )
