from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.core.logging_config import get_logger
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User, UserPreference
from app.schemas.auth import AuthResponse, LoginRequest, SignupRequest, UserOut

router = APIRouter(prefix="/auth", tags=["Auth"])
logger = get_logger(__name__)


def _set_session_cookie(response: Response, user_id: str) -> None:
    token = create_access_token(user_id)
    response.set_cookie(
        key=settings.AUTH_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, response: Response, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An account with this email already exists.")

    user = User(
        email=payload.email.lower(),
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
    )
    db.add(user)
    db.flush()
    db.add(UserPreference(user_id=user.id))
    db.commit()
    db.refresh(user)

    logger.info("New user signed up: %s", user.id)
    _set_session_cookie(response, user.id)
    return AuthResponse(user=UserOut.model_validate(user), access_token_expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password.")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This account has been deactivated.")

    logger.info("User logged in: %s", user.id)
    _set_session_cookie(response, user.id)
    return AuthResponse(user=UserOut.model_validate(user), access_token_expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    response.delete_cookie(settings.AUTH_COOKIE_NAME, path="/")


@router.post("/refresh", response_model=AuthResponse)
def refresh(response: Response, user: User = Depends(get_current_user)):
    """Re-issues the session cookie, extending the sliding expiry while the
    user is active. (A long-lived refresh token isn't held client-side here
    since the whole point of the cookie approach is not exposing tokens to
    JS; the current valid cookie itself is the refresh proof.)"""
    _set_session_cookie(response, user.id)
    return AuthResponse(user=UserOut.model_validate(user), access_token_expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return UserOut.model_validate(user)
