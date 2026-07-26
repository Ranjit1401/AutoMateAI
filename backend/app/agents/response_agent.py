from datetime import datetime

from app.agents.base_agent import BaseAgent


class ResponseAgent(BaseAgent):
    """Formats every specialized agent's output into one readable message.
    Rewritten to handle all seven specialized agents' result shapes
    (travel, research, itinerary, budget, restaurant, maps, booking) —
    the previous version only knew about travel/weather/flights/hotels/
    research and silently dropped everything else."""

    @staticmethod
    def _format_action(action: str) -> str:
        return action.replace("_", " ").title()

    @staticmethod
    def _format_datetime(value: str) -> str:
        try:
            return datetime.fromisoformat(value).strftime("%d %b %Y, %I:%M %p")
        except (ValueError, TypeError):
            return value

    def generate(self, state: dict) -> str:
        execution = state.get("agent_outputs", {}).get("execution", [])
        if not execution:
            return "No results were generated."

        lines: list[str] = ["✅ Here's what I found:", ""]

        for item in execution:
            result = item.get("result", {})
            lines.extend(self._render_result(result))

        lines.append("")
        lines.append("📋 Steps completed:")
        for item in execution:
            lines.append(f"• {self._format_action(item['task']['action'])}")

        return "\n".join(lines).strip()

    def _render_result(self, result: dict) -> list[str]:
        lines: list[str] = []

        if "travel" in result:
            lines.extend(self._render_travel(result))
        if "research" in result:
            lines.extend(self._render_research(result["research"]))
        if "itinerary" in result:
            lines.extend(self._render_itinerary(result["itinerary"]))
        if "budget" in result and result["budget"]:
            lines.extend(self._render_budget(result["budget"]))
        if "restaurants" in result:
            lines.extend(self._render_restaurants(result["restaurants"]))
        if "directions" in result and result["directions"]:
            lines.extend(self._render_directions(result["directions"]))
        if "bookings" in result:
            lines.extend(self._render_bookings(result["bookings"]))

        return lines

    def _render_travel(self, result: dict) -> list[str]:
        travel = result.get("travel", {})
        weather = result.get("weather", {}) or {}
        flights = result.get("flights", []) or []
        hotels = result.get("hotels", []) or []

        lines = [
            f"📍 Source: {travel.get('source', 'N/A')}",
            f"🏝 Destination: {travel.get('destination', 'N/A')}",
            f"💰 Budget: ₹{travel.get('budget', 'N/A')}",
            f"👥 Travellers: {travel.get('travellers', 'N/A')}",
        ]

        if weather and not weather.get("error"):
            lines += [
                "",
                "🌦 Current Weather",
                f"Condition: {weather.get('condition', 'N/A')}",
                f"Temperature: {weather.get('temperature', 'N/A')}°C",
                f"Humidity: {weather.get('humidity', 'N/A')}%",
            ]

        if flights:
            lines += ["", "✈ Available Flights"]
            for f in flights:
                lines += [
                    "",
                    f"Airline : {f.get('airline', 'N/A')}",
                    f"Flight  : {f.get('flight_number', 'N/A')}",
                    f"Price   : ₹{f.get('price', 'N/A')}",
                    f"Departure: {self._format_datetime(f.get('departure', ''))}",
                    f"Arrival  : {self._format_datetime(f.get('arrival', ''))}",
                ]

        if hotels:
            lines += ["", "🏨 Recommended Hotels"]
            for h in hotels:
                lines += ["", f"Hotel : {h.get('name', 'N/A')}", f"Rating: ⭐ {h.get('rating', 'N/A')}", f"Price : {h.get('price', 'Price unavailable')}"]

        lines.append("")
        return lines

    def _render_research(self, research: dict) -> list[str]:
        lines = []
        if research.get("summary"):
            lines += [research["summary"], ""]
        if research.get("top_places"):
            lines += ["📍 Top Places to Visit"] + [f"• {p}" for p in research["top_places"]] + [""]
        if research.get("local_food"):
            lines += ["🍽 Must-Try Local Food"] + [f"• {f}" for f in research["local_food"]] + [""]
        if research.get("best_time"):
            lines += [f"🗓 Best Time to Visit: {research['best_time']}", ""]
        return lines

    def _render_itinerary(self, itinerary: dict) -> list[str]:
        lines = [f"🗺 Itinerary for {itinerary.get('destination', 'N/A')}"]
        for day in itinerary.get("days", []):
            lines.append(f"Day {day['day']}: {day['theme']}")
            lines += [f"  - {a}" for a in day.get("activities", [])]
        lines.append("")
        return lines

    def _render_budget(self, budget: dict) -> list[str]:
        return [
            "💵 Budget Estimate",
            f"Flights: ₹{budget.get('flight_total', 0):.0f}",
            f"Hotel: ₹{budget.get('hotel_total', 0):.0f}",
            f"Daily spend: ₹{budget.get('daily_spend_total', 0):.0f}",
            f"Total: ₹{budget.get('grand_total', 0):.0f} (₹{budget.get('per_traveller', 0):.0f}/traveller)",
            "",
        ]

    def _render_restaurants(self, restaurants: list[dict]) -> list[str]:
        if not restaurants:
            return []
        lines = ["🍴 Recommended Restaurants"]
        for r in restaurants:
            lines.append(f"• {r.get('name', 'N/A')} — ⭐ {r.get('rating', 'N/A')} ({r.get('address', 'N/A')})")
        lines.append("")
        return lines

    def _render_directions(self, directions: dict) -> list[str]:
        return [
            "🧭 Directions",
            f"{directions.get('start_address', 'N/A')} → {directions.get('end_address', 'N/A')}",
            f"Distance: {directions.get('distance', 'N/A')}, Duration: {directions.get('duration', 'N/A')}",
            "",
        ]

    def _render_bookings(self, bookings: list[dict]) -> list[str]:
        if not bookings:
            return []
        lines = ["🎫 Provisional Bookings"]
        for b in bookings:
            lines.append(f"• {b.get('booking_type', 'N/A').title()} — Ref: {b.get('reference', 'N/A')} ({b.get('status', 'N/A')})")
        lines.append("")
        return lines
