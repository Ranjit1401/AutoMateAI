from datetime import datetime, timedelta

from app.agents.base_agent import BaseAgent
from app.prompts.travel_prompt import TRAVEL_PROMPT
from app.schemas.travel import TravelInput
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

        print("=" * 60)
        print("TRAVEL INPUT")
        print(travel.model_dump())
        print("=" * 60)

        # -------------------------
        # Default travel dates
        # -------------------------

        check_in = travel.start_date

        if not check_in:
            check_in = (
                datetime.now() + timedelta(days=7)
            ).strftime("%Y-%m-%d")

        trip_days = travel.days

        check_out = travel.end_date
        
        if not check_out:
            check_out = (
                datetime.strptime(check_in, "%Y-%m-%d")
                + timedelta(days=trip_days)
            ).strftime("%Y-%m-%d")

        # -------------------------
        # Weather
        # -------------------------

        weather = tool_executor.execute(
            "weather",
            city=travel.destination,
        )

        # -------------------------
        # Flights
        # -------------------------

        flights = tool_executor.execute(
            "flight",
            source=travel.source,
            destination=travel.destination,
        )

        # -------------------------
        # Hotels
        # -------------------------

        hotels = tool_executor.execute(
            "hotel",
            destination=travel.destination,
            check_in_date=check_in,
            check_out_date=check_out,
        )

        print("=" * 60)
        print("HOTEL RAW RESULT")
        print(hotels)
        print("=" * 60)

        return {
            "action": action,
            "travel": travel.model_dump(),
            "weather": weather,
            "flights": flights,
            "hotels": hotels,
        }