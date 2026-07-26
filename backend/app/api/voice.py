from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import User
from app.schemas.vapi_schema import StartVoiceSessionRequest
from app.services import log_service, vapi_service
from app.services.vapi_service import VapiServiceError

router = APIRouter(tags=["Voice"])


@router.post("/voice")
def start_voice_session(request: StartVoiceSessionRequest, user: User = Depends(get_current_user)):
    """Starts a Vapi voice session. Pass `customer_number` to place an
    outbound phone call, or omit it to receive a web-call config for the
    frontend's Vapi Web SDK."""
    try:
        return vapi_service.create_call(
            assistant_id=request.assistant_id, customer_number=request.customer_number, metadata=request.metadata,
        )
    except VapiServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/voice/webhook")
async def voice_webhook(request: Request, db: Session = Depends(get_db)):
    """Receives server-side events from Vapi during a call (function calls,
    transcripts, status updates, end-of-call reports). Configure this URL
    as the assistant's `serverUrl` in Vapi."""
    try:
        payload = await request.json()
        result = vapi_service.handle_webhook_event(payload)
    except VapiServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    log_service.add_log(db, "Vapi webhook event received", source="vapi", meta=payload)
    db.commit()
    return result
