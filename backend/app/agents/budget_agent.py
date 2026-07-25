from app.agents.base_agent import BaseAgent
from app.utils.execution_logger import log_step

class BudgetAgent(BaseAgent):

    name = "budget"

    def execute(self, action, state):

        execution = state["agent_outputs"]["execution"]

        travel = {}
        flights = []
        hotels = []

        # Extract travel, flights and hotels
        for item in execution:

            result = item["result"]

            if "travel" in result:
                travel = result["travel"]
                flights = result.get("flights", [])
                hotels = result.get("hotels", [])

        budget_value = travel.get("budget")

        budget = float(budget_value) if budget_value is not None else 0.0

        travellers = int(travel.get("travellers", 1))

        days = int(travel.get("days", 3))

        # --------------------------
        # Flight Cost
        # --------------------------

        flight_cost = 0

        valid_flights = []

        for flight in flights:
        
            price = flight.get("price", 0)

            if isinstance(price, str):
                try:
                    price = float(
                        price.replace("₹", "").replace(",", "")
                    )
                except:
                    continue
                
            if isinstance(price, (int, float)) and price > 0:
                valid_flights.append(price)

        if valid_flights:
            cheapest = min(valid_flights)
            flight_cost = cheapest * travellers

        # --------------------------
        # Hotel Selection
        # --------------------------

        selected_hotel = None
        hotel_cost = 0

        valid_hotels = []

        for hotel in hotels:

            price = hotel.get("price", 0)

            if isinstance(price, str):
                try:
                    price = float(
                        price.replace("₹", "").replace(",", "")
                    )
                except:
                    continue

            if isinstance(price, (int, float)) and price > 0:

                valid_hotels.append({
                    "name": hotel.get("name", "Unknown Hotel"),
                    "rating": hotel.get("rating", "N/A"),
                    "price": float(price)
                })

        # Pick the cheapest hotel
        if valid_hotels:

            valid_hotels.sort(key=lambda x: x["price"])

            selected_hotel = valid_hotels[0]

            hotel_cost = selected_hotel["price"] * days

        # --------------------------
        # Other Costs
        # --------------------------

        food_cost = 1000 * days * travellers

        transport_cost = 500 * days

        activities_cost = 500 * days

        # --------------------------
        # Total Cost
        # --------------------------

        total = (
            flight_cost
            + hotel_cost
            + food_cost
            + transport_cost
            + activities_cost
        )

        remaining = budget - total

        suggestions = []

        if remaining < 0:

            suggestions.append("Choose a cheaper hotel.")
            suggestions.append("Select a lower-cost flight.")
            suggestions.append("Reduce activity expenses.")

        # --------------------------
        # Debug
        # --------------------------

        print("=" * 60)
        print("BUDGET RESULT")
        print({
            "selected_hotel": selected_hotel,
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

        log_step(
            state,
            "Budget Agent",
            "Budget calculated"
        )

        # --------------------------
        # Response
        # --------------------------

        return {
            "budget": {
                "selected_hotel": selected_hotel,
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