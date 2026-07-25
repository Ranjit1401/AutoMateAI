from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class StartVoiceSessionRequest(BaseModel):
    """
    Sent by the frontend to start a voice session.
    If `customer_number` is provided, an outbound phone call is placed
    through Vapi. Otherwise, a web-call config is returned so the frontend
    can start an in-browser call using the Vapi Web SDK.
    """

    assistant_id: Optional[str] = Field(
        default=None,
        description="Vapi assistant id to use. Falls back to VAPI_ASSISTANT_ID if omitted."
    )

    customer_number: Optional[str] = Field(
        default=None,
        description="E.164 phone number to call. Omit for a browser based call."
    )

    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Arbitrary metadata forwarded to Vapi and echoed back in webhooks."
    )


class VapiWebhookPayload(BaseModel):
    """
    Generic wrapper for Vapi server events.
    Vapi sends different event shapes (function-call, status-update,
    end-of-call-report, transcript, etc.) all nested under `message`.
    """

    message: Dict[str, Any]
