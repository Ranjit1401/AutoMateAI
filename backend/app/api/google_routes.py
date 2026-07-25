from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse

from app.schemas.google_schema import (
    SendEmailRequest,
    CreateCalendarEventRequest,
    UploadFileRequest,
    AppendSheetRowRequest,
)
from app.services.google import gmail_service, calendar_service, drive_service, sheets_service
from app.services.google.google_auth import (
    get_authorization_url,
    exchange_code_for_token,
    GoogleAuthError,
)
from app.services.google.gmail_service import GmailServiceError
from app.services.google.calendar_service import CalendarServiceError
from app.services.google.drive_service import DriveServiceError
from app.services.google.sheets_service import SheetsServiceError

router = APIRouter()


# ---------------------------------------------------------------------------
# OAuth
# ---------------------------------------------------------------------------

@router.get("/google/auth")
def google_auth(user_id: str = Query(default="default")):
    """
    Redirects the frontend/browser to Google's consent screen.
    `user_id` is passed through as `state` so the callback knows who to
    associate the resulting tokens with.
    """

    try:
        auth_url = get_authorization_url(state=user_id)
        return RedirectResponse(url=auth_url)

    except GoogleAuthError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/google/oauth/callback")
def google_oauth_callback(code: str, state: str = "default"):
    """
    Google redirects here (GOOGLE_REDIRECT_URI) after the user grants
    consent. Exchanges the auth code for tokens and stores them.
    """

    try:
        exchange_code_for_token(code=code, user_id=state)
        return {"status": "connected", "user_id": state}

    except GoogleAuthError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ---------------------------------------------------------------------------
# Gmail
# ---------------------------------------------------------------------------

@router.post("/gmail/send")
def gmail_send(request: SendEmailRequest):

    try:
        return gmail_service.send_email(
            to=request.to,
            subject=request.subject,
            body=request.body,
            cc=request.cc,
            bcc=request.bcc,
            is_html=request.is_html,
            user_id=request.user_id,
        )

    except GmailServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))


# ---------------------------------------------------------------------------
# Calendar
# ---------------------------------------------------------------------------

@router.post("/calendar/create")
def calendar_create(request: CreateCalendarEventRequest):

    try:
        return calendar_service.create_calendar_event(
            summary=request.summary,
            start_time=request.start_time,
            end_time=request.end_time,
            description=request.description,
            timezone=request.timezone,
            attendees=request.attendees,
            location=request.location,
            user_id=request.user_id,
        )

    except CalendarServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))


# ---------------------------------------------------------------------------
# Drive
# ---------------------------------------------------------------------------

@router.post("/drive/upload")
def drive_upload(request: UploadFileRequest):

    try:
        return drive_service.upload_file(
            file_name=request.file_name,
            file_content_base64=request.file_content_base64,
            mime_type=request.mime_type,
            folder_id=request.folder_id,
            user_id=request.user_id,
        )

    except DriveServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))


# ---------------------------------------------------------------------------
# Sheets
# ---------------------------------------------------------------------------

@router.post("/sheets/append")
def sheets_append(request: AppendSheetRowRequest):

    try:
        return sheets_service.append_sheet_row(
            spreadsheet_id=request.spreadsheet_id,
            values=request.values,
            range_name=request.range_name,
            user_id=request.user_id,
        )

    except SheetsServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
