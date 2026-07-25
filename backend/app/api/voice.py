from fastapi import APIRouter, HTTPException, Request

from app.schemas.vapi_schema import StartVoiceSessionRequest
from app.services import vapi_service
from app.services.vapi_service import VapiServiceError

router = APIRouter()


@router.post("/voice")
def start_voice_session(request: StartVoiceSessionRequest):
    """
    Starts a Vapi voice session.

    - Pass `customer_number` to place an outbound phone call.
    - Omit it to receive a web-call config for the frontend's Vapi Web SDK.
    """

    try:
        call = vapi_service.create_call(
            assistant_id=request.assistant_id,
            customer_number=request.customer_number,
            metadata=request.metadata,
        )
        return call

    except VapiServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@router.post("/voice/webhook")
async def voice_webhook(request: Request):
    """
    Receives server-side events from Vapi during a call (function calls,
    transcripts, status updates, end-of-call reports).

    Configure this URL as the assistant's `serverUrl` in Vapi so it knows
    where to send events for a given call.
    """

    try:
        payload = await request.json()
        result = vapi_service.handle_webhook_event(payload)
        return result

    except VapiServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
