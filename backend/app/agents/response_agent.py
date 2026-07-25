from datetime import datetime
from app.utils.execution_logger import log_step
from app.agents.base_agent import BaseAgent


class ResponseAgent(BaseAgent):

    @staticmethod
    def format_action(action: str) -> str:
        """
        Convert machine-friendly action names into readable text.
        Example:
        book_flight_from_Mumbai_to_Goa
        ->
        Book Flight From Mumbai To Goa
        """
        return action.replace("_", " ").title()

    @staticmethod
    def format_datetime(value: str) -> str:
        """
        Convert ISO datetime into a readable format.
        Example:
        2026-08-05 22:10
        ->
        05 Aug 2026, 10:10 PM
        """
        try:
            return datetime.fromisoformat(value).strftime(
                "%d %b %Y, %I:%M %p"
            )
        except Exception:
            return value

    def generate(self, state):
        budget_result = None

        execution = state.get("agent_outputs", {}).get("execution", [])

        if not execution:
            return "No results were generated."

        travel_result = None
        research_result = None
        itinerary_result = None

        for item in execution:

            result = item.get("result", {})

            if "travel" in result:
                travel_result = result

            if "research" in result:
                research_result = result

            if "itinerary" in result:
                itinerary_result = result

            if "budget" in result:
                budget_result = result

        if not travel_result:
            return "Travel information could not be generated."

        travel = travel_result.get("travel", {})
        weather = travel_result.get("weather", {})
        flights = travel_result.get("flights", [])
        hotels = travel_result.get("hotels", [])
        itinerary = {}

        if itinerary_result:
            itinerary = itinerary_result.get("itinerary", {})

        lines = []

        ##########################################################
        # HEADER
        ##########################################################

        lines.append("✅ Your travel plan is ready!")
        lines.append("")

        lines.append(f"📍 Source: {travel.get('source', 'N/A')}")
        lines.append(f"🏝 Destination: {travel.get('destination', 'N/A')}")
        lines.append(f"💰 Budget: ₹{travel.get('budget', 'N/A')}")
        lines.append(f"👥 Travellers: {travel.get('travellers', 'N/A')}")

        ##########################################################
        # WEATHER
        ##########################################################

        if weather:

            lines.append("")
            lines.append("🌦 Current Weather")

            lines.append(
                f"Condition: {weather.get('condition', 'N/A')}"
            )

            lines.append(
                f"Temperature: {weather.get('temperature', 'N/A')}°C"
            )

            lines.append(
                f"Humidity: {weather.get('humidity', 'N/A')}%"
            )

            lines.append(
                f"Wind Speed: {weather.get('wind_speed', 'N/A')} m/s"
            )

        ##########################################################
        # FLIGHTS
        ##########################################################

        if flights:

            lines.append("")
            lines.append("✈ Available Flights")

            for flight in flights:

                departure = self.format_datetime(
                    flight.get("departure", "")
                )

                arrival = self.format_datetime(
                    flight.get("arrival", "")
                )

                lines.append("")

                lines.append(
                    f"Airline : {flight.get('airline', 'N/A')}"
                )

                lines.append(
                    f"Flight  : {flight.get('flight_number', 'N/A')}"
                )

                lines.append(
                    f"Price   : ₹{flight.get('price', 'N/A')}"
                )

                lines.append(
                    f"Departure: {departure}"
                )

                lines.append(
                    f"Arrival  : {arrival}"
                )

                lines.append(
                    f"Duration : {flight.get('duration', 'N/A')} mins"
                )

        ##########################################################
        # HOTELS
        ##########################################################

        if hotels:

            lines.append("")
            lines.append("🏨 Recommended Hotels")

            for hotel in hotels:

                lines.append("")

                lines.append(
                    f"Hotel : {hotel.get('name', 'N/A')}"
                )

                lines.append(
                    f"Rating: ⭐ {hotel.get('rating', 'N/A')}"
                )

                lines.append(
                    f"Price : {hotel.get('price', 'Price unavailable')}"
                )

        ##########################################################
        # PLANNED TASKS
        ##########################################################

        lines.append("")
        lines.append("📋 Planned Tasks")

        for item in execution:

            action = self.format_action(
                item["task"]["action"]
            )

            lines.append(f"• {action}")

        ##########################################################
        # RESEARCH
        ##########################################################

        if research_result:

            research = research_result["research"]

            top_places = research.get(
                "top_places",
                []
            )

            if top_places:

                lines.append("")
                lines.append("📍 Top Places to Visit")

                for place in top_places:
                    lines.append(f"• {place}")

            foods = research.get(
                "local_food",
                []
            )

            if foods:

                lines.append("")
                lines.append("🍽 Must-Try Local Food")

                for food in foods:
                    lines.append(f"• {food}")

            lines.append("")
            lines.append(
                f"🗓 Best Time to Visit: "
                f"{research.get('best_time', 'N/A')}"
            )

            if budget_result:

                budget = budget_result["budget"]
            
                lines.append("")
                lines.append("💰 Budget Analysis")
            
                lines.append(f"Flight Cost : ₹{budget['flight_cost']:.2f}")
                lines.append(f"Hotel Cost : ₹{budget['hotel_cost']:.2f}")
                lines.append(f"Food Cost : ₹{budget['food_cost']:.2f}")
                lines.append(f"Transport Cost : ₹{budget['transport_cost']:.2f}")
                lines.append(f"Activities Cost : ₹{budget['activities_cost']:.2f}")
            
                lines.append("")
                lines.append(f"Estimated Total : ₹{budget['total_cost']:.2f}")
                lines.append(f"Budget : ₹{budget['budget']:.2f}")
            
                if budget["within_budget"]:
                    lines.append(
                        f"✅ Remaining Budget : ₹{budget['remaining_budget']:.2f}"
                    )
                else:
                    lines.append(
                        f"❌ Over Budget by : ₹{abs(budget['remaining_budget']):.2f}"
                    )
            
                    if budget["suggestions"]:
                        lines.append("")
                        lines.append("Suggestions")
            
                        for suggestion in budget["suggestions"]:
                            lines.append(f"• {suggestion}")

        ##########################################################
        # FOOTER
        ##########################################################

        lines.append("")
        lines.append("🎉 Have a safe and enjoyable journey!")

        if itinerary:

            lines.append("")
            lines.append("📅 Itinerary")
        
            for day in itinerary:
            
                lines.append("")
                lines.append(f"Day {day.get('day', 'N/A')}")
                lines.append(f"🌅 Morning : {day.get('morning', 'N/A')}")
                lines.append(f"🌞 Afternoon : {day.get('afternoon', 'N/A')}")
                lines.append(f"🌙 Evening : {day.get('evening', 'N/A')}")
        
        log_step(
            state,
            "Response Agent",
            "Final response generated"
        )
        
        return "\n".join(lines)