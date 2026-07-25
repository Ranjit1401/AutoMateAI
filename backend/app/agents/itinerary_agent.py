from app.agents.base_agent import BaseAgent
from app.utils.execution_logger import log_step

class ItineraryAgent(BaseAgent):

    name = "itinerary"

    from app.agents.base_agent import BaseAgent


class ItineraryAgent(BaseAgent):

    name = "itinerary"

    def execute(self, action: str, state: dict):

        execution = state["agent_outputs"]["execution"]

        travel = {}
        research = {}

        # Read outputs from previous agents
        for item in execution:

            result = item["result"]

            if "travel" in result:
                travel = result["travel"]

            if "research" in result:
                research = result["research"]

        destination = travel.get("destination", "Unknown")
        days = travel.get("days", 3)

        places = research.get("top_places", [])
        foods = research.get("local_food", [])

        itinerary = []

        for day in range(days):

            morning = ""
            afternoon = ""
            evening = ""

            if places:
                morning = places[day % len(places)]

            if len(places) > 1:
                afternoon = places[(day + 1) % len(places)]

            if foods:
                evening = f"Enjoy {foods[day % len(foods)]}"
            else:
                evening = f"Explore local food in {destination}"

            itinerary.append({
                "day": day + 1,
                "morning": morning,
                "afternoon": afternoon,
                "evening": evening
            })

            log_step(
                state,
                "Itinerary Agent",
                "Itinerary generated"
            )

        return {
            "destination": destination,
            "days": days,
            "itinerary": itinerary
        }