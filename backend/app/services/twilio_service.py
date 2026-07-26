from typing import Any, Dict, Optional

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from twilio.request_validator import RequestValidator

from app.core.config import settings


class TwilioServiceError(Exception):
    """Raised whenever a call to the Twilio API fails."""


def _get_client() -> Client:

    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        raise TwilioServiceError("TWILIO_ACCOUNT_SID / TWILIO_AUTH_TOKEN are not configured.")

    return Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def make_outgoing_call(
    to_number: str,
    from_number: Optional[str] = None,
    twiml_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Places an outbound call. `twiml_url` should point at a publicly
    reachable endpoint (e.g. this service's /call/incoming route, or any
    URL returning TwiML) that Twilio will fetch once the call connects.
    """

    caller_id = from_number or settings.TWILIO_PHONE_NUMBER

    if not caller_id:
        raise TwilioServiceError("No from_number provided and TWILIO_PHONE_NUMBER is not configured.")

    if not twiml_url:
        raise TwilioServiceError("twiml_url is required to place an outgoing call.")

    try:
        client = _get_client()

        call = client.calls.create(
            to=to_number,
            from_=caller_id,
            url=twiml_url,
        )

        return {
            "call_sid": call.sid,
            "status": call.status,
            "to": call.to,
            "from": call._from,
        }

    except TwilioRestException as exc:
        raise TwilioServiceError(f"Failed to place outgoing call: {exc}") from exc


def send_sms(
    to_number: str,
    message: str,
    from_number: Optional[str] = None,
) -> Dict[str, Any]:

    sender = from_number or settings.TWILIO_PHONE_NUMBER

    if not sender:
        raise TwilioServiceError("No from_number provided and TWILIO_PHONE_NUMBER is not configured.")

    try:
        client = _get_client()

        sms = client.messages.create(
            to=to_number,
            from_=sender,
            body=message,
        )

        return {
            "message_sid": sms.sid,
            "status": sms.status,
            "to": sms.to,
        }

    except TwilioRestException as exc:
        raise TwilioServiceError(f"Failed to send SMS: {exc}") from exc


def validate_webhook_signature(url: str, params: Dict[str, Any], signature: str) -> bool:
    """
    Verifies that an incoming webhook request genuinely came from Twilio.
    Use this inside the /call/incoming and /call/status route handlers
    before trusting the request body, when TWILIO_VALIDATE_SIGNATURE=true.
    """

    if not settings.TWILIO_AUTH_TOKEN:
        raise TwilioServiceError("TWILIO_AUTH_TOKEN is not configured.")

    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
    return validator.validate(url, params, signature)


def build_voice_response(message: str) -> str:
    """
    Builds a minimal TwiML <Response> that speaks `message` to the caller.
    Returned as the body of the /call/incoming webhook.
    """

    from twilio.twiml.voice_response import VoiceResponse

    response = VoiceResponse()
    response.say(message)
    return str(response)
