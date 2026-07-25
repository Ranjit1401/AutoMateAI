from app.agents.base_agent import BaseAgent


class ItineraryAgent(BaseAgent):

    name = "itinerary"

    def execute(self, action: str, state: dict):

        travel = state.get("travel", {})
        research = state.get("research", {})

        destination = travel.get("destination", "Unknown")
        days = travel.get("days", 3)

        places = research.get("top_places", [])

        itinerary = []

        place_index = 0

        for day in range(1, days + 1):

            day_plan = {
                "day": day,
                "morning": "",
                "afternoon": "",
                "evening": ""
            }

            if place_index < len(places):
                day_plan["morning"] = places[place_index]
                place_index += 1

            if place_index < len(places):
                day_plan["afternoon"] = places[place_index]
                place_index += 1

            day_plan["evening"] = f"Explore local food in {destination}"

            itinerary.append(day_plan)

        return {
            "destination": destination,
            "days": days,
            "itinerary": itinerary
        }