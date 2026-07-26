from app.agents.base_agent import BaseAgent
from app.core.logging_config import get_logger
from app.schemas.planner import PlannerResponse

logger = get_logger(__name__)

_AVAILABLE_AGENTS = (
    "travel (weather/flights/hotels), research (attractions/food/best time), "
    "itinerary (day-by-day plan), budget (cost estimate), restaurant "
    "(nearby dining), maps (directions/distance), booking (reserve a pick)"
)


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.planner = self.llm.with_structured_output(PlannerResponse)

    def plan(self, user_input: str, task_type: str) -> PlannerResponse:
        prompt = f"""You are an AI Planning Agent for a travel assistant.

Task Type:
{task_type}

Available specialized agents and what each does:
{_AVAILABLE_AGENTS}

User Request:
{user_input}

Break the request into a short, ordered list of concrete steps. Word each
step so it clearly indicates which specialized agent should handle it
(e.g. include the word "budget" for a budget step, "restaurant" for a
dining step, "itinerary" for a day-plan step, "book"/"reserve" for a
booking step, "direction"/"route" for a maps step)."""

        try:
            return self.planner.invoke(prompt)
        except Exception:  # noqa: BLE001 - LLM unavailable must not crash the pipeline
            logger.exception("Planner LLM call failed; using fallback plan.")
            from app.agents.fallback_data import fallback_planner_response

            return fallback_planner_response()
