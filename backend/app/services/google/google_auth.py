"""Google OAuth flow + credential storage.

Tokens are persisted in the GoogleToken table (see app/db/models.py),
scoped strictly to the requesting user_id. The previous version stored
tokens in a process-RAM dict and silently fell back to "whichever token
was stored first" when no exact user_id match existed — a real
multi-tenant data leak. That fallback has been removed entirely: no
matching row means the caller must (re)connect their own account.
"""
from typing import Any

from google.auth.transport.requests import Request as GoogleAuthRequest
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import GoogleToken


class GoogleAuthError(Exception):
    """Raised when Google OAuth configuration or token exchange fails."""


def _client_config() -> dict[str, Any]:
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise GoogleAuthError("GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET are not configured.")

    return {
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }


def get_authorization_url(state: str) -> str:
    """Builds the URL the frontend should redirect the user to in order to
    grant Gmail/Calendar/Drive/Sheets access. `state` is the app's own
    user id, so the callback knows whose account to attach tokens to."""
    flow = Flow.from_client_config(_client_config(), scopes=settings.GOOGLE_SCOPES, redirect_uri=settings.GOOGLE_REDIRECT_URI)
    auth_url, _ = flow.authorization_url(access_type="offline", include_granted_scopes="true", prompt="consent", state=state)
    return auth_url


def exchange_code_for_token(db: Session, code: str, user_id: str) -> GoogleToken:
    flow = Flow.from_client_config(_client_config(), scopes=settings.GOOGLE_SCOPES, redirect_uri=settings.GOOGLE_REDIRECT_URI)
    flow.fetch_token(code=code)
    credentials = flow.credentials

    token = db.get(GoogleToken, user_id)
    if token is None:
        token = GoogleToken(user_id=user_id)
        db.add(token)

    token.access_token = credentials.token
    token.refresh_token = credentials.refresh_token or (token.refresh_token if token.refresh_token else None)
    token.token_uri = credentials.token_uri
    token.client_id = credentials.client_id
    token.client_secret = credentials.client_secret
    token.scopes = " ".join(credentials.scopes or [])

    db.commit()
    db.refresh(token)
    return token


def get_credentials(db: Session, user_id: str) -> Credentials:
    """Loads this user's stored credentials and refreshes them if expired.
    Raises if this exact user has not connected an account — never falls
    back to another user's token."""
    token = db.get(GoogleToken, user_id)
    if token is None:
        raise GoogleAuthError("No Google account connected for this user. Complete the OAuth flow first.")

    credentials = Credentials(
        token=token.access_token,
        refresh_token=token.refresh_token,
        token_uri=token.token_uri,
        client_id=token.client_id,
        client_secret=token.client_secret,
        scopes=token.scopes.split(),
    )

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(GoogleAuthRequest())
        token.access_token = credentials.token
        db.commit()

    return credentials
