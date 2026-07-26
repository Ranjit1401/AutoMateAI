"""
DEPRECATED shim — re-exports from app.api.deps (the canonical auth module).

The application now uses dual-transport auth: httpOnly cookie for same-origin
dev, and Authorization: Bearer header for cross-origin production deployments.

All imports should come from app.api.deps directly.
"""
from app.api.deps import get_current_user, get_db, get_optional_user  # noqa: F401

__all__ = ["get_db", "get_current_user", "get_optional_user"]
