from datetime import datetime

from app.agents.base_agent import BaseAgent
from app.agents.mixins import TravelExtractionMixin
from app.schemas.itinerary import ItineraryPlan


class ItineraryAgent(BaseAgent, TravelExtractionMixin):
    """Generates a real, destination-specific day-by-day itinerary via the
    LLM's structured output — not a static template."""

    def __init__(self):
        super().__init__()
        self._itinerary_parser = self.llm.with_structured_output(ItineraryPlan)

    def execute(self, action: str, state: dict) -> dict:
        travel = self.extract_travel(state["user_input"])
        nights = self._nights(travel)

        prompt = (
            f"Create a {nights}-day travel itinerary for {travel.destination}. "
            f"Travellers: {travel.travellers}. "
            "Each day should have a short theme and 3-5 concrete, ordered activities."
        )
        plan = self._itinerary_parser.invoke(prompt)

        return {
            "action": action,
            "itinerary": {"destination": travel.destination, "days": [d.model_dump() for d in plan.days]},
        }

    @staticmethod
    def _nights(travel) -> int:
        if travel.start_date and travel.end_date:
            try:
                start = datetime.fromisoformat(travel.start_date).date()
                end = datetime.fromisoformat(travel.end_date).date()
                return max((end - start).days, 1)
            except ValueError:
                pass
        return 3
