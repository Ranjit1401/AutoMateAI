from typing import Optional

from pydantic import BaseModel, Field


class OutgoingCallRequest(BaseModel):

    to_number: str = Field(description="E.164 destination phone number, e.g. +14155551234")

    from_number: Optional[str] = Field(
        default=None,
        description="Caller id to use. Falls back to TWILIO_PHONE_NUMBER if omitted."
    )

    twiml_url: Optional[str] = Field(
        default=None,
        description="Publicly reachable URL Twilio should fetch TwiML from once the call connects."
    )


class SmsRequest(BaseModel):

    to_number: str = Field(description="E.164 destination phone number")

    message: str = Field(description="SMS body text")

    from_number: Optional[str] = Field(
        default=None,
        description="Sender number. Falls back to TWILIO_PHONE_NUMBER if omitted."
    )
