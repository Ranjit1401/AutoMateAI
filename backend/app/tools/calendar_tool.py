"""Registers Google Calendar as an agent-callable tool (previously only
exposed as a raw REST endpoint in app/api/google_routes.py, never wired
into the agent/tool pipeline). Requires the calling user to have connected
their Google account (see /google/auth); if they haven't, this returns a
graceful, structured "not connected" result instead of raising.
"""
from app.services.google import calendar_service
from app.services.google.calendar_service import CalendarServiceError
from app.tools.base import BaseTool, ToolError


class CalendarTool(BaseTool):
    name = "calendar"
    description = "Creates an event on the authenticated user's connected Google Calendar."

    def execute(
        self,
        summary: str,
        start_time: str,
        end_time: str,
        *,
        db=None,
        user_id: str | None = None,
        **kwargs,
    ) -> dict:
        if db is None or user_id is None:
            return {
                "status": "not_connected",
                "note": "Calendar requires a signed-in user with Google connected (see /google/auth).",
            }
        try:
            return calendar_service.create_calendar_event(
                summary=summary, start_time=start_time, end_time=end_time, db=db, user_id=user_id, **kwargs
            )
        except CalendarServiceError as exc:
            return {"status": "failed", "note": f"Calendar event creation failed: {exc}"}
        except Exception as exc:  # noqa: BLE001 - never let an unconfigured Google account crash the run
            return {"status": "not_connected", "note": f"Calendar unavailable: {exc}"}
