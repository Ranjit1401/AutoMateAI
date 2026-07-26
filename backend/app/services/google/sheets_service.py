from typing import Any, Dict, List, Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from sqlalchemy.orm import Session

from app.services.google.google_auth import get_credentials, GoogleAuthError


class SheetsServiceError(Exception):
    """Raised when a Sheets API call fails."""


def append_sheet_row(
    spreadsheet_id: str,
    values: List[str],
    range_name: str = "Sheet1!A1",
    *,
    db: Session,
    user_id: str,
) -> Dict[str, Any]:
    """
    Appends a single row of `values` to `spreadsheet_id`, right after the
    last row of data found in `range_name`.
    """

    try:
        credentials = get_credentials(db, user_id)
        service = build("sheets", "v4", credentials=credentials)

        body = {"values": [values]}

        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body,
        ).execute()

        return {
            "updated_range": result.get("updates", {}).get("updatedRange"),
            "updated_rows": result.get("updates", {}).get("updatedRows"),
        }

    except GoogleAuthError as exc:
        raise SheetsServiceError(str(exc)) from exc

    except HttpError as exc:
        raise SheetsServiceError(f"Sheets API error: {exc}") from exc
