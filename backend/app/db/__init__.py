from app.db.base import Base, SessionLocal, engine, get_db  # noqa: F401
from app.db import models  # noqa: F401  (ensures models are registered on Base.metadata)


def init_db() -> None:
    """Create tables that don't exist yet. Safe to call repeatedly.

    For SQLite this is sufficient for local/dev use out of the box. If you
    migrate to Postgres for production, run the Alembic migrations in
    backend/alembic/ instead of relying on this (see backend/alembic/README).
    """
    Base.metadata.create_all(bind=engine)
