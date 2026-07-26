from app.agents.base_agent import BaseAgent
from app.agents.mixins import TravelExtractionMixin
from app.tools.executor import ToolExecutionError, tool_executor


class RestaurantAgent(BaseAgent, TravelExtractionMixin):
    """Finds real, highly-rated restaurants near the trip destination via
    Google Places (see app/tools/restaurant_tool.py)."""

    def execute(self, action: str, state: dict) -> dict:
        travel = self.extract_travel(state["user_input"])
        try:
            restaurants = tool_executor.execute("restaurant", destination=travel.destination)
        except ToolExecutionError as exc:
            return {"action": action, "restaurants": [], "error": exc.message}

        return {"action": action, "restaurants": restaurants}
