from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import PlainTextResponse

from app.schemas.twilio_schema import OutgoingCallRequest, SmsRequest
from app.services import twilio_service
from app.services.twilio_service import TwilioServiceError

router = APIRouter()


@router.post("/call")
def create_outgoing_call(request: OutgoingCallRequest):
    """
    Places an outbound phone call via Twilio.
    `twiml_url` should point at a URL returning TwiML (e.g. /call/incoming
    on this same service, hosted at a publicly reachable BASE_URL).
    """

    try:
        result = twilio_service.make_outgoing_call(
            to_number=request.to_number,
            from_number=request.from_number,
            twiml_url=request.twiml_url,
        )
        return result

    except TwilioServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@router.post("/sms")
def send_sms(request: SmsRequest):
    """Sends an SMS message via Twilio."""

    try:
        result = twilio_service.send_sms(
            to_number=request.to_number,
            message=request.message,
            from_number=request.from_number,
        )
        return result

    except TwilioServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@router.post("/call/incoming")
async def incoming_call_webhook(request: Request):
    """
    Twilio calls this when someone dials your Twilio number.
    Returns TwiML telling Twilio what to say/do next.
    """

    # Example of validating the request came from Twilio (optional, enable
    # via TWILIO_VALIDATE_SIGNATURE=true once BASE_URL is publicly reachable):
    #
    # signature = request.headers.get("X-Twilio-Signature", "")
    # form = await request.form()
    # is_valid = twilio_service.validate_webhook_signature(str(request.url), dict(form), signature)
    # if not is_valid:
    #     raise HTTPException(status_code=403, detail="Invalid Twilio signature")

    twiml = twilio_service.build_voice_response(
        "Thanks for calling. Please hold while we connect you to our assistant."
    )
    return PlainTextResponse(content=twiml, media_type="application/xml")


@router.post("/call/status")
async def call_status_webhook(request: Request):
    """
    Twilio calls this to report call lifecycle events
    (initiated, ringing, answered, completed).
    """

    form = await request.form()
    call_sid = form.get("CallSid")
    call_status = form.get("CallStatus")

    # Placeholder: persist call status updates as needed (DB, logs, etc.)
    return {"call_sid": call_sid, "status": call_status}
