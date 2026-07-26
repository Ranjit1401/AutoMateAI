from app.agents.base_agent import BaseAgent
from app.agents.mixins import TravelExtractionMixin
from app.tools.executor import ToolExecutionError, tool_executor


class BookingAgent(BaseAgent, TravelExtractionMixin):
    """Creates a provisional booking record for the cheapest available
    flight and hotel for the trip (see app/tools/booking_tool.py for the
    honest scope note on why this doesn't finalize a real purchase)."""

    def execute(self, action: str, state: dict) -> dict:
        travel = self.extract_travel(state["user_input"])
        bookings: list[dict] = []
        errors: list[str] = []

        try:
            flights = tool_executor.execute("flight", source=travel.source or "Mumbai", destination=travel.destination)
            if flights:
                bookings.append(
                    tool_executor.execute("booking", booking_type="flight", details=flights[0])
                )
        except ToolExecutionError as exc:
            errors.append(exc.message)

        try:
            hotels = tool_executor.execute("hotel", destination=travel.destination)
            if hotels:
                bookings.append(
                    tool_executor.execute("booking", booking_type="hotel", details=hotels[0])
                )
        except ToolExecutionError as exc:
            errors.append(exc.message)

        return {"action": action, "bookings": bookings, "errors": errors}
