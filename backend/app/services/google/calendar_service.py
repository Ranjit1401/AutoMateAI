from typing import Any, Dict, List, Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from sqlalchemy.orm import Session

from app.services.google.google_auth import get_credentials, GoogleAuthError


class CalendarServiceError(Exception):
    """Raised when a Calendar API call fails."""


def create_calendar_event(
    summary: str,
    start_time: str,
    end_time: str,
    description: Optional[str] = None,
    timezone: str = "UTC",
    attendees: Optional[List[str]] = None,
    location: Optional[str] = None,
    *,
    db: Session,
    user_id: str,
) -> Dict[str, Any]:
    """
    Creates an event on the authenticated user's primary calendar.
    `start_time` / `end_time` are ISO 8601 datetimes, e.g. 2026-08-01T10:00:00
    """

    try:
        credentials = get_credentials(db, user_id)
        service = build("calendar", "v3", credentials=credentials)

        event_body: Dict[str, Any] = {
            "summary": summary,
            "start": {"dateTime": start_time, "timeZone": timezone},
            "end": {"dateTime": end_time, "timeZone": timezone},
        }

        if description:
            event_body["description"] = description

        if location:
            event_body["location"] = location

        if attendees:
            event_body["attendees"] = [{"email": email} for email in attendees]

        created = service.events().insert(
            calendarId="primary",
            body=event_body,
        ).execute()

        return {
            "event_id": created.get("id"),
            "html_link": created.get("htmlLink"),
            "status": created.get("status"),
        }

    except GoogleAuthError as exc:
        raise CalendarServiceError(str(exc)) from exc

    except HttpError as exc:
        raise CalendarServiceError(f"Calendar API error: {exc}") from exc
