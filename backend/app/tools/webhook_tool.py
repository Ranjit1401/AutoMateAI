"""Generic outbound webhook trigger — n8n-compatible (and works with Zapier,
Make, or any other webhook-driven automation tool). Configure
N8N_WEBHOOK_URL to point at your n8n Webhook node's Production URL."""
import requests

from app.core.config import settings
from app.tools.base import BaseTool, ToolError


class WebhookTriggerTool(BaseTool):
    name = "webhook_trigger"
    description = "Triggers a configured n8n (or other automation platform) webhook with a JSON payload."

    def execute(self, event: str, payload: dict) -> dict:
        if not settings.N8N_WEBHOOK_URL:
            raise ToolError("N8N_WEBHOOK_URL is not configured.")

        headers = {"Content-Type": "application/json"}
        if settings.N8N_WEBHOOK_TOKEN:
            headers["Authorization"] = f"Bearer {settings.N8N_WEBHOOK_TOKEN}"

        try:
            response = requests.post(
                settings.N8N_WEBHOOK_URL,
                json={"event": event, "payload": payload},
                headers=headers,
                timeout=15,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise ToolError(f"Webhook trigger failed: {exc}") from exc

        return {"triggered": True, "status_code": response.status_code}
