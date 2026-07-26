from datetime import datetime

from app.agents.base_agent import BaseAgent
from app.agents.mixins import TravelExtractionMixin
from app.core.logging_config import get_logger
from app.schemas.itinerary import ItineraryPlan

logger = get_logger(__name__)


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
        try:
            plan = self._itinerary_parser.invoke(prompt)
        except Exception:  # noqa: BLE001 - LLM unavailable must not crash the pipeline
            logger.exception("Itinerary LLM call failed; using fallback itinerary.")
            from app.agents.fallback_data import fallback_itinerary_plan

            plan = fallback_itinerary_plan(nights)

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
