from app.agents.base_agent import BaseAgent
from app.schemas.travel import TravelInput
from app.schemas.research import ResearchOutput
from app.prompts.travel_prompt import TRAVEL_PROMPT
from app.utils.execution_logger import log_step


class ResearchAgent(BaseAgent):

    def __init__(self):
        super().__init__()
        self.travel_parser = self.llm.with_structured_output(TravelInput)
        self.research_parser = self.llm.with_structured_output(ResearchOutput)

    def extract(self, user_input: str) -> TravelInput:

        prompt = f"""
{TRAVEL_PROMPT}

User Request:
{user_input}
"""

        return self.travel_parser.invoke(prompt)

    def execute(self, action: str, state):

        travel = self.extract(state["user_input"])

        destination = travel.destination

        prompt = f"""
You are an expert travel researcher.

Research the city "{destination}".

Return:
- best time to visit
- 5 famous tourist attractions
- 3 must-try local foods

Respond only with structured data.
"""

        research = self.research_parser.invoke(prompt)

        log_step(
            state,
            "Research Agent",
            "Tourist information collected"
        )

        return {
            "action": action,
            "research": {
                "destination": destination,
                "best_time": research.best_time,
                "top_places": research.top_places,
                "local_food": research.local_food,
            },
        }