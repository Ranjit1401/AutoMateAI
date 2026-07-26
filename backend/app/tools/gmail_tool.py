"""Registers Gmail as an agent-callable tool (previously only exposed as a
raw REST endpoint in app/api/google_routes.py, never wired into the
agent/tool pipeline). Requires the calling user to have connected their
Google account (see /google/auth); if they haven't, this returns a
graceful, structured "not connected" result instead of raising, so a demo
run without Google OAuth configured never crashes the pipeline.
"""
from app.services.google import gmail_service
from app.services.google.gmail_service import GmailServiceError
from app.tools.base import BaseTool, ToolError


class GmailTool(BaseTool):
    name = "gmail"
    description = "Sends an email via the authenticated user's connected Gmail account."

    def execute(self, to: str, subject: str, body: str, *, db=None, user_id: str | None = None, **kwargs) -> dict:
        if db is None or user_id is None:
            return {
                "status": "not_connected",
                "note": "Gmail requires a signed-in user with Google connected (see /google/auth).",
            }
        try:
            return gmail_service.send_email(to=to, subject=subject, body=body, db=db, user_id=user_id, **kwargs)
        except GmailServiceError as exc:
            return {"status": "failed", "note": f"Gmail send failed: {exc}"}
        except Exception as exc:  # noqa: BLE001 - never let an unconfigured Google account crash the run
            return {"status": "not_connected", "note": f"Gmail unavailable: {exc}"}
