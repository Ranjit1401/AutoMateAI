from app.agents.base_agent import BaseAgent
from app.schemas.travel import TravelInput
from app.prompts.travel_prompt import TRAVEL_PROMPT
from app.tools.executor import tool_executor


class TravelAgent(BaseAgent):

    def __init__(self):
        super().__init__()
        self.parser = self.llm.with_structured_output(TravelInput)

    def extract(self, user_input: str) -> TravelInput:
        """
        Extract structured travel information from the ORIGINAL user request.
        """

        prompt = f"""
{TRAVEL_PROMPT}

User Request:
{user_input}
"""

        return self.parser.invoke(prompt)

    def execute(self, action: str, state):

        travel = self.extract(state["user_input"])

        weather = tool_executor.execute(
            "weather",
            city=travel.destination,
        )
        
        flights = tool_executor.execute(
            "flight",
            source=travel.source,
            destination=travel.destination,
        )
        
        hotels = tool_executor.execute(
            "hotel",
            destination=travel.destination,
        )

        return {
            "action": action,
            "travel": travel.model_dump(),
            "weather": weather,
            "flights": flights,
            "hotels": hotels
        }