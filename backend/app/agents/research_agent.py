from app.agents.base_agent import BaseAgent
from app.schemas.travel import TravelInput
from app.prompts.travel_prompt import TRAVEL_PROMPT


class ResearchAgent(BaseAgent):

    def __init__(self):
        super().__init__()
        self.parser = self.llm.with_structured_output(TravelInput)

    def extract(self, user_input: str) -> TravelInput:

        prompt = f"""
{TRAVEL_PROMPT}

User Request:
{user_input}
"""

        return self.parser.invoke(prompt)

    def execute(self, action: str, state):

        travel = self.extract(state["user_input"])

        destination = travel.destination

        return {
            "action": action,
            "research": {
                "destination": destination,
                "best_time": "November to February",
                "top_places": [
                    "Baga Beach",
                    "Fort Aguada",
                    "Dudhsagar Falls",
                    "Anjuna Beach",
                    "Basilica of Bom Jesus"
                ],
                "local_food": [
                    "Goan Fish Curry",
                    "Prawn Balchão",
                    "Bebinca"
                ]
            }
        }