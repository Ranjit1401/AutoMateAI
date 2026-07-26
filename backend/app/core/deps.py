"""
DEPRECATED — this file previously used HTTPBearer (Authorization header) for
auth. The application now uses httpOnly cookie-based sessions exclusively.

All imports that used to come from here should now come from app.api.deps,
which reads the session cookie set by /auth/login and /auth/signup.

This shim re-exports everything so any legacy import path still works without
a code change on the caller side.
"""
from app.api.deps import get_current_user, get_db, get_optional_user  # noqa: F401

__all__ = ["get_db", "get_current_user", "get_optional_user"]
