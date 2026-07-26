"""
Auth service — business logic for signup, login, and token refresh.
Keeps route handlers thin.
"""
import logging
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse

logger = logging.getLogger(__name__)


class AuthError(Exception):
    """Domain-level authentication error."""


def signup(request: SignupRequest, db: Session) -> tuple[User, TokenResponse]:
    """
    Create a new user.
    Raises AuthError if the email is already registered.
    """
    existing = db.query(User).filter(User.email == request.email.lower()).first()
    if existing:
        raise AuthError("An account with this email already exists.")

    user = User(
        email=request.email.lower(),
        name=request.name,
        hashed_password=hash_password(request.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info("New user registered: %s", user.email)
    tokens = _issue_tokens(user)
    return user, tokens


def login(request: LoginRequest, db: Session) -> tuple[User, TokenResponse]:
    """
    Authenticate an existing user.
    Raises AuthError for wrong email or password.
    """
    user = db.query(User).filter(User.email == request.email.lower()).first()

    if not user or not verify_password(request.password, user.hashed_password):
        raise AuthError("Invalid email or password.")

    if not user.is_active:
        raise AuthError("This account has been deactivated.")

    logger.info("User logged in: %s", user.email)
    tokens = _issue_tokens(user)
    return user, tokens


def refresh_tokens(refresh_token: str, db: Session) -> TokenResponse:
    """
    Issue a new access + refresh token pair from a valid refresh token.
    Raises AuthError if the refresh token is invalid or expired.
    """
    payload = decode_token(refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise AuthError("Invalid or expired refresh token.")

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()

    if not user or not user.is_active:
        raise AuthError("User not found or inactive.")

    return _issue_tokens(user)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _issue_tokens(user: User) -> TokenResponse:
    data = {"sub": user.id}
    return TokenResponse(
        access_token=create_access_token(data),
        refresh_token=create_refresh_token(data),
    )
