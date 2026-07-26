"""
Shared FastAPI dependencies: DB session access and the current-user guard
used to protect every non-public route.

Auth is carried in a signed, httpOnly cookie (see app/api/auth.py) rather
than a bearer header, so the frontend never handles raw JWTs in JS.
"""
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import TokenError, decode_token
from app.db import get_db
from app.db.models import User

__all__ = ["get_db", "get_current_user", "get_optional_user"]


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


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """Raises 401 if there is no valid, non-expired session cookie."""
    token = request.cookies.get(settings.AUTH_COOKIE_NAME)
    user = _load_user(token, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user


def get_optional_user(request: Request, db: Session = Depends(get_db)) -> User | None:
    """Like get_current_user but returns None instead of raising — for
    routes that behave differently when logged in vs anonymous."""
    token = request.cookies.get(settings.AUTH_COOKIE_NAME)
    return _load_user(token, db)
