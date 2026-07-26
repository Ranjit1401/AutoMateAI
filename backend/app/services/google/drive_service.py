import base64
import io
from typing import Any, Dict, Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

from sqlalchemy.orm import Session

from app.services.google.google_auth import get_credentials, GoogleAuthError


class DriveServiceError(Exception):
    """Raised when a Drive API call fails."""


def upload_file(
    file_name: str,
    file_content_base64: str,
    mime_type: str = "application/octet-stream",
    folder_id: Optional[str] = None,
    *,
    db: Session,
    user_id: str,
) -> Dict[str, Any]:
    """
    Uploads a base64 encoded file to the authenticated user's Google Drive.
    """

    try:
        credentials = get_credentials(db, user_id)
        service = build("drive", "v3", credentials=credentials)

        file_bytes = base64.b64decode(file_content_base64)
        media = MediaIoBaseUpload(io.BytesIO(file_bytes), mimetype=mime_type, resumable=True)

        file_metadata: Dict[str, Any] = {"name": file_name}

        if folder_id:
            file_metadata["parents"] = [folder_id]

        uploaded = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, name, webViewLink",
        ).execute()

        return {
            "file_id": uploaded.get("id"),
            "name": uploaded.get("name"),
            "web_view_link": uploaded.get("webViewLink"),
        }

    except GoogleAuthError as exc:
        raise DriveServiceError(str(exc)) from exc

    except HttpError as exc:
        raise DriveServiceError(f"Drive API error: {exc}") from exc
