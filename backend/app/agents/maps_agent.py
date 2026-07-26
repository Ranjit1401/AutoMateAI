from app.agents.base_agent import BaseAgent
from app.agents.mixins import TravelExtractionMixin
from app.tools.executor import ToolExecutionError, tool_executor


class MapsAgent(BaseAgent, TravelExtractionMixin):
    """Gets real driving directions/distance/duration between the trip's
    source and destination via Google Maps (see app/tools/maps_tool.py)."""

    def execute(self, action: str, state: dict) -> dict:
        travel = self.extract_travel(state["user_input"])
        origin = travel.source or "Mumbai"

        try:
            directions = tool_executor.execute("maps", origin=origin, destination=travel.destination)
        except ToolExecutionError as exc:
            return {"action": action, "directions": None, "error": exc.message}

        return {"action": action, "directions": directions}
