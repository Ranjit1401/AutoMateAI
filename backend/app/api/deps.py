"""
Shared FastAPI dependencies: DB session access and the current-user guard
used to protect every non-public route.

Auth is carried in TWO possible transports to support both local dev and
cross-origin production deployments:

1. httpOnly cookie (automateai_session) — preferred for same-origin dev.
2. Authorization: Bearer <token> header — used in production where the
   browser's third-party cookie policy (ITP, Privacy Sandbox, ETP) blocks
   cross-site cookies even with SameSite=None; Secure.

The dependency checks the cookie first, then falls back to the Bearer header.
The frontend stores the token in localStorage and sends it as a Bearer header.
"""
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import TokenError, decode_token
from app.db import get_db
from app.db.models import User

__all__ = ["get_db", "get_current_user", "get_optional_user"]

# auto_error=False so we can fall back to the cookie without FastAPI raising.
_bearer = HTTPBearer(auto_error=False)


def _load_user(token: str | None, db: Session) -> User | None:
    if not token:
        return None
    try:
        payload = decode_token(token, expected_type="access")
    except TokenError:
        return None

    user = db.get(User, payload.get("sub"))
    if user is None or not user.is_active:
        return None
    return user


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User:
    """Raises 401 if there is no valid, non-expired session.

    Checks in order:
    1. httpOnly session cookie (works in same-origin / local dev)
    2. Authorization: Bearer header (works in cross-origin production where
       the browser blocks third-party cookies)
    """
    # 1 — cookie
    token = request.cookies.get(settings.AUTH_COOKIE_NAME)
    user = _load_user(token, db)
    if user:
        return user

    # 2 — Bearer header fallback
    if credentials:
        user = _load_user(credentials.credentials, db)
    if user:
        return user

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")


def get_optional_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User | None:
    """Like get_current_user but returns None instead of raising."""
    token = request.cookies.get(settings.AUTH_COOKIE_NAME)
    user = _load_user(token, db)
    if user:
        return user
    if credentials:
        return _load_user(credentials.credentials, db)
    return None
