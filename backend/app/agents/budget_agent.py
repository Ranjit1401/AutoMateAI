from app.agents.base_agent import BaseAgent


class BudgetAgent(BaseAgent):

    name = "budget"

    def execute(self, action, state):

        execution = state["agent_outputs"]["execution"]

        travel = {}
        flights = []
        hotels = []

        for item in execution:

            result = item["result"]

            if "travel" in result:
                travel = result["travel"]
                flights = result.get("flights", [])
                hotels = result.get("hotels", [])

        budget = float(travel.get("budget", 0))

        travellers = int(travel.get("travellers", 1))

        days = int(travel.get("days", 3))

        flight_cost = 0

        if flights:
            flight_cost = flights[0].get("price", 0)

        hotel_cost = 0

        if hotels:

            hotel_price = hotels[0].get("price", 0)

            if isinstance(hotel_price, str):
                hotel_price = (
                    hotel_price
                    .replace("₹", "")
                    .replace(",", "")
                )

            hotel_cost = float(hotel_price) * days

        food_cost = 1000 * days * travellers

        transport_cost = 500 * days

        activities_cost = 500 * days

        total = (
            flight_cost +
            hotel_cost +
            food_cost +
            transport_cost +
            activities_cost
        )

        remaining = budget - total

        suggestions = []

        if remaining < 0:

            suggestions.append(
                "Choose a cheaper hotel."
            )
        
            suggestions.append(
                "Select a lower-cost flight."
            )
        
        print("=" * 60)
        print("BUDGET RESULT")
        print({
            "flight_cost": flight_cost,
            "hotel_cost": hotel_cost,
            "food_cost": food_cost,
            "transport_cost": transport_cost,
            "activities_cost": activities_cost,
            "total": total,
            "budget": budget,
            "remaining": remaining,
        })
        print("=" * 60)

        return {
            "budget": {
                "flight_cost": flight_cost,
                "hotel_cost": hotel_cost,
                "food_cost": food_cost,
                "transport_cost": transport_cost,
                "activities_cost": activities_cost,
                "total_cost": total,
                "budget": budget,
                "remaining_budget": remaining,
                "within_budget": remaining >= 0,
                "suggestions": suggestions,
            }
        }