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
        Extract structured travel information from the user's request.
        """
        prompt = f"""
{TRAVEL_PROMPT}

User Request:
{user_input}
"""

        return self.parser.invoke(prompt)

    def execute(self, action: str, state: dict):
        """
        Execute the travel task assigned by the supervisor.
        """

        # Extract structured travel details
        travel = self.extract(action)

        # Get weather using the Tool Executor
        weather = tool_executor.execute(
            tool_name="weather",
            city=travel.destination
        )

        # Return the combined result
        return {
            "travel": travel.model_dump(),
            "weather": weather
        }