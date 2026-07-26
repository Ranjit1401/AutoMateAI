from typing import Any, Dict, Optional

import requests

from app.core.config import settings


class VapiServiceError(Exception):
    """Raised whenever a call to the Vapi API fails."""


def _headers() -> Dict[str, str]:

    if not settings.VAPI_API_KEY:
        raise VapiServiceError("VAPI_API_KEY is not configured.")

    return {
        "Authorization": f"Bearer {settings.VAPI_API_KEY}",
        "Content-Type": "application/json",
    }


def get_default_assistant_config() -> Dict[str, Any]:
    """
    Returns a starter assistant configuration. This can be sent to
    `create_assistant` or referenced directly when starting a call.
    Tune model/voice/prompt as needed for your use case.
    """

    return {
        "name": "assistant",
        "firstMessage": "Hi, thanks for calling. How can I help you today?",
        "model": {
            "provider": "openai",
            "model": "gpt-4o",
            "temperature": 0.3,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful voice assistant. Keep responses short and conversational."
                }
            ],
        },
        "voice": {
            "provider": "11labs",
            "voiceId": "rachel",
        },
        "serverUrl": None,  # set at call/creation time to point at /voice/webhook
        "endCallFunctionEnabled": True,
    }


def create_assistant(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Creates a persistent Vapi assistant using `config`, falling back to
    `get_default_assistant_config()` when no config is supplied.
    """

    payload = config or get_default_assistant_config()

    try:
        response = requests.post(
            f"{settings.VAPI_BASE_URL}/assistant",
            headers=_headers(),
            json=payload,
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as exc:
        raise VapiServiceError(f"Failed to create Vapi assistant: {exc}") from exc


def create_call(
    assistant_id: Optional[str] = None,
    customer_number: Optional[str] = None,
    phone_number_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Starts a Vapi call.

    - If `customer_number` is provided, Vapi places an outbound phone call
      to that number using `phone_number_id` (or VAPI_PHONE_NUMBER_ID).
    - If `customer_number` is omitted, the returned payload contains the
      web-call config the frontend can use with the Vapi Web SDK.
    """

    assistant = assistant_id or settings.VAPI_ASSISTANT_ID

    if not assistant:
        raise VapiServiceError("No assistant_id provided and VAPI_ASSISTANT_ID is not configured.")

    payload: Dict[str, Any] = {"assistantId": assistant}

    if metadata:
        payload["metadata"] = metadata

    if customer_number:
        number_id = phone_number_id or settings.VAPI_PHONE_NUMBER_ID

        if not number_id:
            raise VapiServiceError("phone_number_id is required to place an outbound call.")

        payload["phoneNumberId"] = number_id
        payload["customer"] = {"number": customer_number}

    try:
        response = requests.post(
            f"{settings.VAPI_BASE_URL}/call",
            headers=_headers(),
            json=payload,
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as exc:
        raise VapiServiceError(f"Failed to create Vapi call: {exc}") from exc


def get_call(call_id: str) -> Dict[str, Any]:

    try:
        response = requests.get(
            f"{settings.VAPI_BASE_URL}/call/{call_id}",
            headers=_headers(),
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as exc:
        raise VapiServiceError(f"Failed to fetch Vapi call {call_id}: {exc}") from exc


def end_call(call_id: str) -> Dict[str, Any]:

    try:
        response = requests.patch(
            f"{settings.VAPI_BASE_URL}/call/{call_id}",
            headers=_headers(),
            json={"status": "ended"},
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as exc:
        raise VapiServiceError(f"Failed to end Vapi call {call_id}: {exc}") from exc


def handle_webhook_event(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dispatches an incoming Vapi server event (delivered to /voice/webhook).

    Vapi wraps every event under payload["message"]["type"], e.g.:
    "function-call", "status-update", "end-of-call-report", "transcript".

    This function should NOT talk to the LangGraph agent directly -
    wire the "function-call" branch below into the existing
    app.graph.workflow.graph if/when voice needs to trigger agent logic.
    """

    message = payload.get("message", {})
    event_type = message.get("type")

    if event_type == "function-call":
        function_call = message.get("functionCall", {})
        function_name = function_call.get("name")
        parameters = function_call.get("parameters", {})

        # Placeholder response. Replace with real routing to your
        # existing agent/tool layer if a voice call needs to invoke it.
        return {
            "result": f"Function '{function_name}' received with parameters {parameters}."
        }

    if event_type == "end-of-call-report":
        # Placeholder: persist call summary/transcript if needed.
        return {"status": "received"}

    if event_type == "status-update":
        return {"status": "received"}

    if event_type == "transcript":
        return {"status": "received"}

    return {"status": "ignored", "type": event_type}
