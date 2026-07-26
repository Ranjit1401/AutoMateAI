from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.db.models import GoogleToken, User
from app.schemas.google_schema import (
    AppendSheetRowRequest,
    CreateCalendarEventRequest,
    SendEmailRequest,
    UploadFileRequest,
)
from app.services.google import calendar_service, drive_service, gmail_service, sheets_service
from app.services.google.calendar_service import CalendarServiceError
from app.services.google.drive_service import DriveServiceError
from app.services.google.google_auth import GoogleAuthError, exchange_code_for_token, get_authorization_url
from app.services.google.gmail_service import GmailServiceError
from app.services.google.sheets_service import SheetsServiceError

router = APIRouter(tags=["Google"])


# ---------------------------------------------------------------------------
# OAuth
# ---------------------------------------------------------------------------

@router.get("/google/auth")
def google_auth(user: User = Depends(get_current_user)):
    """Redirects to Google's consent screen. The authenticated user's id is
    passed as `state`, so the callback below knows whose account to attach
    the resulting tokens to — this can no longer be spoofed via a query
    param the way the old `?user_id=` version could."""
    try:
        return RedirectResponse(url=get_authorization_url(state=user.id))
    except GoogleAuthError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/google/oauth/callback")
def google_oauth_callback(code: str, state: str, db: Session = Depends(get_db)):
    """Google redirects here (GOOGLE_REDIRECT_URI) after consent."""
    try:
        exchange_code_for_token(db, code=code, user_id=state)
    except GoogleAuthError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return RedirectResponse(url=f"{settings.FRONTEND_URL}/apps?google=connected")


# ---------------------------------------------------------------------------
# Gmail
# ---------------------------------------------------------------------------

@router.post("/gmail/send")
def gmail_send(request: SendEmailRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return gmail_service.send_email(
            to=request.to, subject=request.subject, body=request.body,
            cc=request.cc, bcc=request.bcc, is_html=request.is_html,
            db=db, user_id=user.id,
        )
    except GmailServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


# ---------------------------------------------------------------------------
# Calendar
# ---------------------------------------------------------------------------

@router.post("/calendar/create")
def calendar_create(request: CreateCalendarEventRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return calendar_service.create_calendar_event(
            summary=request.summary, start_time=request.start_time, end_time=request.end_time,
            description=request.description, timezone=request.timezone,
            attendees=request.attendees, location=request.location,
            db=db, user_id=user.id,
        )
    except CalendarServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


# ---------------------------------------------------------------------------
# Drive
# ---------------------------------------------------------------------------

@router.post("/drive/upload")
def drive_upload(request: UploadFileRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return drive_service.upload_file(
            file_name=request.file_name, file_content_base64=request.file_content_base64,
            mime_type=request.mime_type, folder_id=request.folder_id,
            db=db, user_id=user.id,
        )
    except DriveServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


# ---------------------------------------------------------------------------
# Sheets
# ---------------------------------------------------------------------------

@router.post("/sheets/append")
def sheets_append(request: AppendSheetRowRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return sheets_service.append_sheet_row(
            spreadsheet_id=request.spreadsheet_id, values=request.values, range_name=request.range_name,
            db=db, user_id=user.id,
        )
    except SheetsServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/google/status")
def google_status(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    connected = db.get(GoogleToken, user.id) is not None
    return {"connected": connected}
