from app.agents.base_agent import BaseAgent
from app.agents.mixins import TravelExtractionMixin
from app.tools.executor import ToolExecutionError, tool_executor


class TravelAgent(BaseAgent, TravelExtractionMixin):
    """Extracts trip details and fetches live weather, flights, and hotels."""

    def execute(self, action: str, state: dict) -> dict:
        travel = self.extract_travel(state["user_input"])

        result = {"action": action, "travel": travel.model_dump()}

        for tool_name, kwargs, key in (
            ("weather", {"city": travel.destination}, "weather"),
            ("flight", {"source": travel.source, "destination": travel.destination}, "flights"),
            ("hotel", {"destination": travel.destination}, "hotels"),
        ):
            try:
                result[key] = tool_executor.execute(tool_name, **kwargs)
            except ToolExecutionError as exc:
                result[key] = {"error": exc.message} if key == "weather" else []

        return result
