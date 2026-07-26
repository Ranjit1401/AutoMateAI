from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.core.logging_config import get_logger
from app.db.models import User
from app.schemas.twilio_schema import OutgoingCallRequest, SmsRequest
from app.services import log_service, twilio_service
from app.services.twilio_service import TwilioServiceError

router = APIRouter(tags=["Calls"])
logger = get_logger(__name__)


@router.post("/call")
def create_outgoing_call(request: OutgoingCallRequest, user: User = Depends(get_current_user)):
    """Places an outbound phone call via Twilio. `twiml_url` should point at
    a URL returning TwiML (e.g. /call/incoming on this service, hosted at a
    publicly reachable BASE_URL)."""
    try:
        return twilio_service.make_outgoing_call(
            to_number=request.to_number, from_number=request.from_number, twiml_url=request.twiml_url,
        )
    except TwilioServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/sms")
def send_sms(request: SmsRequest, user: User = Depends(get_current_user)):
    try:
        return twilio_service.send_sms(
            to_number=request.to_number, message=request.message, from_number=request.from_number,
        )
    except TwilioServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


async def _verify_twilio_signature(request: Request) -> dict:
    form = await request.form()
    if settings.TWILIO_VALIDATE_SIGNATURE:
        signature = request.headers.get("X-Twilio-Signature", "")
        if not twilio_service.validate_webhook_signature(str(request.url), dict(form), signature):
            raise HTTPException(status_code=403, detail="Invalid Twilio signature")
    return dict(form)


@router.post("/call/incoming")
async def incoming_call_webhook(request: Request):
    """Twilio calls this when someone dials your Twilio number. Signature
    validation is enforced whenever TWILIO_VALIDATE_SIGNATURE=true (the
    default) — the previous version had this check written but commented
    out, meaning the webhook accepted unauthenticated requests by default."""
    await _verify_twilio_signature(request)

    twiml = twilio_service.build_voice_response("Thanks for calling. Please hold while we connect you to our assistant.")
    return PlainTextResponse(content=twiml, media_type="application/xml")


@router.post("/call/status")
async def call_status_webhook(request: Request, db: Session = Depends(get_db)):
    """Twilio calls this to report call lifecycle events (initiated,
    ringing, answered, completed). Now actually persisted instead of being
    a no-op placeholder."""
    form = await _verify_twilio_signature(request)
    call_sid = form.get("CallSid")
    call_status = form.get("CallStatus")

    log_service.add_log(
        db, f"Twilio call {call_sid} status: {call_status}", source="twilio",
        meta={"call_sid": call_sid, "status": call_status},
    )
    db.commit()
    return {"call_sid": call_sid, "status": call_status}
