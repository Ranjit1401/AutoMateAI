from app.agents.base_agent import BaseAgent
from app.agents.mixins import TravelExtractionMixin
from app.schemas.research import DestinationResearch


class ResearchAgent(BaseAgent, TravelExtractionMixin):
    """Generates destination research (attractions, food, best time to
    visit) via the LLM, tailored to the actual extracted destination —
    unlike the previous version, which returned the same hardcoded Goa
    data for every request regardless of where the user was going."""

    def __init__(self):
        super().__init__()
        self._research_parser = self.llm.with_structured_output(DestinationResearch)

    def research(self, destination: str) -> DestinationResearch:
        prompt = (
            "You are a travel research assistant. Provide accurate, specific "
            f"information about visiting {destination}.\n"
            "Only include real places and dishes associated with this destination."
        )
        return self._research_parser.invoke(prompt)

    def execute(self, action: str, state: dict) -> dict:
        travel = self.extract_travel(state["user_input"])
        research = self.research(travel.destination)

        return {
            "action": action,
            "research": {
                "destination": travel.destination,
                "best_time": research.best_time_to_visit,
                "top_places": research.top_places,
                "local_food": research.local_food,
                "summary": research.summary,
            },
        }
