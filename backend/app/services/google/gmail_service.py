import base64
from email.mime.text import MIMEText
from typing import Any, Dict, List, Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.services.google.google_auth import get_credentials, GoogleAuthError


class GmailServiceError(Exception):
    """Raised when a Gmail API call fails."""


def send_email(
    to: str,
    subject: str,
    body: str,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
    is_html: bool = False,
    user_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Sends an email through the authenticated user's Gmail account.
    """

    try:
        credentials = get_credentials(user_id)
        service = build("gmail", "v1", credentials=credentials)

        mime_message = MIMEText(body, "html" if is_html else "plain")
        mime_message["to"] = to
        mime_message["subject"] = subject

        if cc:
            mime_message["cc"] = ", ".join(cc)

        if bcc:
            mime_message["bcc"] = ", ".join(bcc)

        raw_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

        sent = service.users().messages().send(
            userId="me",
            body={"raw": raw_message},
        ).execute()

        return {"message_id": sent.get("id"), "status": "sent"}

    except GoogleAuthError as exc:
        raise GmailServiceError(str(exc)) from exc

    except HttpError as exc:
        raise GmailServiceError(f"Gmail API error: {exc}") from exc
