from typing import Any, Dict, Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleAuthRequest

from app.config.settings import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
    GOOGLE_SCOPES,
)


class GoogleAuthError(Exception):
    """Raised when Google OAuth configuration or token exchange fails."""


# ---------------------------------------------------------------------------
# Placeholder token store.
#
# Replace this with real persistence (DB table, Redis, etc.) keyed by your
# app's user id. Kept in-memory here only so the OAuth flow is runnable
# end-to-end out of the box.
# ---------------------------------------------------------------------------
_TOKEN_STORE: Dict[str, Dict[str, Any]] = {}


def _client_config() -> Dict[str, Any]:

    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET or not GOOGLE_REDIRECT_URI:
        raise GoogleAuthError(
            "GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET / GOOGLE_REDIRECT_URI are not configured."
        )

    return {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uris": [GOOGLE_REDIRECT_URI],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }


def get_authorization_url(state: Optional[str] = None) -> str:
    """
    Builds the URL the frontend should redirect the user to in order to
    grant Gmail/Calendar/Drive/Sheets access.
    """

    flow = Flow.from_client_config(
        _client_config(),
        scopes=GOOGLE_SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI,
    )

    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
        state=state,
    )

    return auth_url


def exchange_code_for_token(code: str, user_id: str) -> Dict[str, Any]:
    """
    Exchanges the OAuth `code` returned to GOOGLE_REDIRECT_URI for tokens,
    and stores them against `user_id`. Call this from the
    /google/oauth/callback route.
    """

    flow = Flow.from_client_config(
        _client_config(),
        scopes=GOOGLE_SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI,
    )

    flow.fetch_token(code=code)
    credentials = flow.credentials

    token_data = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

    _TOKEN_STORE[user_id] = token_data
    return token_data


def save_user_token(user_id: str, token_data: Dict[str, Any]) -> None:
    _TOKEN_STORE[user_id] = token_data


def get_credentials(user_id: Optional[str] = None) -> Credentials:
    """
    Loads stored credentials for `user_id` (or the only stored user, if a
    single-tenant setup) and refreshes them if expired.
    """

    if not _TOKEN_STORE:
        raise GoogleAuthError("No Google account has been connected yet. Complete the OAuth flow first.")

    if user_id and user_id in _TOKEN_STORE:
        token_data = _TOKEN_STORE[user_id]
    else:
        # Single-tenant fallback: use the first (and likely only) stored token.
        token_data = next(iter(_TOKEN_STORE.values()))

    credentials = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri=token_data.get("token_uri"),
        client_id=token_data.get("client_id"),
        client_secret=token_data.get("client_secret"),
        scopes=token_data.get("scopes"),
    )

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(GoogleAuthRequest())

        if user_id:
            token_data["token"] = credentials.token
            _TOKEN_STORE[user_id] = token_data

    return credentials
