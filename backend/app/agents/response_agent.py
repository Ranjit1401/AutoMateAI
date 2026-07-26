"""
ResponseAgent — upgraded to render the full autonomous agent output.

Now includes:
  ✓ Summary
  ✓ Budget breakdown
  ✓ Day-by-day Itinerary with Google Maps links
  ✓ Live Weather (always from OpenWeather)
  ✓ Real Sources (from Tavily — no more "Source: None")
  ✓ Google Maps links for every attraction
  ✓ Google Flights link / MakeMyTrip link
  ✓ Booking.com / Agoda / Google Hotels link
  ✓ Tool execution log showing what actually ran
"""
import urllib.parse
from datetime import datetime

from app.agents.base_agent import BaseAgent


class ResponseAgent(BaseAgent):
    """Formats every specialized agent's output into one readable message."""

    @staticmethod
    def _format_action(action: str) -> str:
        return action.replace("_", " ").title()

    @staticmethod
    def _format_datetime(value: str) -> str:
        try:
            return datetime.fromisoformat(value).strftime("%d %b %Y, %I:%M %p")
        except (ValueError, TypeError):
            return value

    @staticmethod
    def _maps_search_url(place: str, destination: str = "") -> str:
        query = f"{place}, {destination}" if destination else place
        return f"https://www.google.com/maps/search/{urllib.parse.quote(query)}"

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def generate(self, state: dict) -> str:
        execution = state.get("agent_outputs", {}).get("execution", [])
        if not execution:
            return "No results were generated."

        lines: list[str] = ["✅ **AutoMateAI — Trip Planner Report**", ""]

        # Collect all structured data across all agent outputs
        all_research:    dict  = {}
        all_travel:      dict  = {}
        all_weather:     dict  = {}
        all_flights:     list  = []
        all_hotels:      list  = []
        all_itinerary:   dict  = {}
        all_budget:      dict  = {}
        all_restaurants: list  = []
        all_directions:  dict  = {}
        all_bookings:    list  = []
        tool_log:        list[str] = []

        for item in execution:
            result    = item.get("result", {})
            task_name = self._format_action(item["task"]["action"])

            if "error" in result and len(result) == 1:
                tool_log.append(f"❌ {task_name} — failed")
                continue

            tool_log.append(f"✅ {task_name}")

            if "travel" in result:
                all_travel   = result.get("travel", {})
                all_weather  = result.get("weather", {}) or {}
                all_flights  = result.get("flights", []) or []
                all_hotels   = result.get("hotels", []) or []
                if all_flights:
                    tool_log.append("  ↳ ✈ Flight data fetched")
                if all_hotels:
                    tool_log.append("  ↳ 🏨 Hotel data fetched")
                if all_weather and not all_weather.get("error"):
                    tool_log.append("  ↳ 🌦 OpenWeather API called")

            if "research" in result:
                all_research = result["research"]
                tool_used    = all_research.get("tool_used", "LLM")
                tool_log.append(f"  ↳ 🔍 Research via {tool_used}")
                if all_research.get("sources"):
                    tool_log.append(f"  ↳ 📎 {len(all_research['sources'])} real sources found")

            if "itinerary" in result:
                all_itinerary = result["itinerary"]

            if "budget" in result and result["budget"]:
                all_budget = result["budget"]

            if "restaurants" in result:
                all_restaurants = result["restaurants"]
                tool_used_r = result.get("tool_used", "")
                if tool_used_r:
                    tool_log.append(f"  ↳ 🍴 Restaurants via {tool_used_r}")

            if "directions" in result and result["directions"]:
                all_directions = result["directions"]
                if all_directions.get("maps_url"):
                    tool_log.append("  ↳ 🗺 Google Maps link generated")

            if "bookings" in result:
                all_bookings = result["bookings"]

        # -----------------------------------------------------------------------
        # 1. Trip Summary Header
        # -----------------------------------------------------------------------
        destination = (
            all_travel.get("destination")
            or all_research.get("destination")
            or all_itinerary.get("destination")
            or "your destination"
        )
        source       = all_travel.get("source") or "your city"
        budget_val   = all_travel.get("budget")
        travellers   = all_travel.get("travellers", 1)

        lines += [
            "## 🏝 Trip Summary",
            f"**From:** {source}",
            f"**To:** {destination}",
        ]
        if budget_val:
            lines.append(f"**Budget:** ₹{budget_val:,}")
        if travellers:
            lines.append(f"**Travellers:** {travellers}")
        if all_travel.get("start_date"):
            lines.append(f"**Dates:** {all_travel['start_date']} → {all_travel.get('end_date', '')}")
        lines.append("")

        # -----------------------------------------------------------------------
        # 2. Research summary + Sources
        # -----------------------------------------------------------------------
        if all_research:
            lines += self._render_research(all_research, destination)

        # -----------------------------------------------------------------------
        # 3. Weather
        # -----------------------------------------------------------------------
        if all_weather and not all_weather.get("error"):
            lines += self._render_weather(all_weather)

        # -----------------------------------------------------------------------
        # 4. Itinerary with Google Maps links
        # -----------------------------------------------------------------------
        if all_itinerary:
            lines += self._render_itinerary(all_itinerary, destination)

        # -----------------------------------------------------------------------
        # 5. Budget breakdown
        # -----------------------------------------------------------------------
        if all_budget:
            lines += self._render_budget(all_budget)

        # -----------------------------------------------------------------------
        # 6. Flights (real links or live data)
        # -----------------------------------------------------------------------
        if all_flights:
            lines += self._render_flights(all_flights, source, destination)

        # -----------------------------------------------------------------------
        # 7. Hotels (real links or live data)
        # -----------------------------------------------------------------------
        if all_hotels:
            lines += self._render_hotels(all_hotels, destination)

        # -----------------------------------------------------------------------
        # 8. Restaurants with Maps links
        # -----------------------------------------------------------------------
        if all_restaurants:
            lines += self._render_restaurants(all_restaurants, destination)

        # -----------------------------------------------------------------------
        # 9. Directions + Maps link
        # -----------------------------------------------------------------------
        if all_directions:
            lines += self._render_directions(all_directions, source, destination)

        # -----------------------------------------------------------------------
        # 10. Bookings
        # -----------------------------------------------------------------------
        if all_bookings:
            lines += self._render_bookings(all_bookings, destination)

        # -----------------------------------------------------------------------
        # 11. Real Sources (Tavily)
        # -----------------------------------------------------------------------
        sources = all_research.get("sources") or []
        if sources:
            lines += self._render_sources(sources)

        # -----------------------------------------------------------------------
        # 12. Tool Execution Log
        # -----------------------------------------------------------------------
        lines += ["---", "## 🛠 Tool Execution Log", ""]
        lines += [f"  {entry}" for entry in tool_log]
        lines.append("")

        return "\n".join(lines).strip()

    # ------------------------------------------------------------------
    # Section renderers
    # ------------------------------------------------------------------

    def _render_research(self, research: dict, destination: str) -> list[str]:
        lines: list[str] = []
        if research.get("summary"):
            lines += ["## 📖 About the Destination", research["summary"], ""]
        if research.get("top_places"):
            lines += ["### 📍 Top Places to Visit"]
            for place in research["top_places"]:
                maps_link = self._maps_search_url(place, destination)
                lines.append(f"- **{place}** — [📍 View on Maps]({maps_link})")
            lines.append("")
        if research.get("local_food"):
            lines += ["### 🍽 Must-Try Local Food"]
            for food in research["local_food"]:
                lines.append(f"- {food}")
            lines.append("")
        if research.get("best_time"):
            lines += [f"### 🗓 Best Time to Visit", research["best_time"], ""]
        return lines

    def _render_weather(self, weather: dict) -> list[str]:
        note = weather.get("note", "")
        lines = [
            "## 🌦 Current Weather",
            f"**City:** {weather.get('city', 'N/A')}",
            f"**Condition:** {weather.get('condition', 'N/A')}",
            f"**Temperature:** {weather.get('temperature', 'N/A')}°C",
            f"**Humidity:** {weather.get('humidity', 'N/A')}%",
            f"**Wind Speed:** {weather.get('wind_speed', 'N/A')} m/s",
        ]
        if note:
            lines.append(f"*{note}*")
        lines.append("")
        return lines

    def _render_itinerary(self, itinerary: dict, destination: str) -> list[str]:
        lines = [f"## 🗺 Itinerary for {itinerary.get('destination', destination)}", ""]
        for day in itinerary.get("days", []):
            lines.append(f"### Day {day['day']}: {day['theme']}")
            for activity in day.get("activities", []):
                # Try to generate a Maps link for each activity that looks like a place
                maps_link = ""
                if any(kw in activity.lower() for kw in [
                    "visit", "beach", "temple", "fort", "market", "museum",
                    "park", "church", "mosque", "palace", "lake", "waterfall",
                    "restaurant", "café", "cafe", "shack",
                ]):
                    maps_link = f" — [📍 Maps]({self._maps_search_url(activity, destination)})"
                lines.append(f"- {activity}{maps_link}")
            lines.append("")
        return lines

    def _render_budget(self, budget: dict) -> list[str]:
        return [
            "## 💵 Budget Estimate",
            f"- **Flights:** ₹{budget.get('flight_total', 0):,.0f}",
            f"- **Hotel:** ₹{budget.get('hotel_total', 0):,.0f}",
            f"- **Daily Expenses:** ₹{budget.get('daily_spend_total', 0):,.0f}",
            f"- **Total:** ₹{budget.get('grand_total', 0):,.0f}",
            f"- **Per Traveller:** ₹{budget.get('per_traveller', 0):,.0f}",
            "",
        ]

    def _render_flights(self, flights: list[dict], source: str, destination: str) -> list[str]:
        lines = ["## ✈ Flights"]

        # Detect if these are real search links or live SerpAPI data
        has_live = any(f.get("type") == "live" for f in flights)
        has_links = any(f.get("type") == "search_link" for f in flights)

        if has_links:
            lines.append("Search for real-time prices on these platforms:")
            lines.append("")
            for f in flights:
                if f.get("type") == "search_link":
                    url = f.get("search_url", "")
                    airline = f.get("airline", "")
                    desc = f.get("description", "")
                    if url:
                        lines.append(f"- **[{airline}]({url})** — {desc}")
                elif f.get("type") == "info":
                    lines.append(f"\n> ℹ {f.get('description', '')}\n")
        elif has_live:
            lines.append("")
            for f in flights:
                src_url = f.get("source_url", "")
                link_md = f" — [Book]({src_url})" if src_url else ""
                lines += [
                    f"**{f.get('airline', 'N/A')}** {f.get('flight_number', '')}",
                    f"  Departure: {self._format_datetime(f.get('departure', ''))}",
                    f"  Arrival:   {self._format_datetime(f.get('arrival', ''))}",
                    f"  Price:     ₹{f.get('price', 'N/A')}{link_md}",
                    "",
                ]

        lines.append("")
        return lines

    def _render_hotels(self, hotels: list[dict], destination: str) -> list[str]:
        lines = ["## 🏨 Hotels"]

        has_links = any(h.get("type") == "search_link" for h in hotels)

        if has_links:
            lines.append("Browse real hotels on these platforms:")
            lines.append("")
            for h in hotels:
                url  = h.get("url", "")
                name = h.get("name", "")
                desc = h.get("description", "")
                if url:
                    lines.append(f"- **[{name}]({url})** — {desc}")
        else:
            # Live SerpAPI results
            for h in hotels:
                name = h.get("name", "N/A")
                url  = h.get("url", "")
                name_md = f"[{name}]({url})" if url else name
                lines += [
                    f"- **{name_md}** ⭐ {h.get('rating', 'N/A')} — {h.get('price', 'N/A')}",
                ]

        lines.append("")
        return lines

    def _render_restaurants(self, restaurants: list[dict], destination: str) -> list[str]:
        if not restaurants:
            return []
        lines = ["## 🍴 Recommended Restaurants", ""]
        for r in restaurants:
            name    = r.get("name", "N/A")
            rating  = r.get("rating")
            cuisine = r.get("cuisine", "")
            maps_url = r.get("maps_url") or self._maps_search_url(name, destination)
            src_url  = r.get("source_url", "")
            src_name = r.get("source", "")

            rating_str  = f" ⭐ {rating}" if rating else ""
            cuisine_str = f" ({cuisine})" if cuisine else ""
            src_str     = f" — [Source: {src_name}]({src_url})" if src_url and src_name else ""

            lines.append(
                f"- **[{name}]({maps_url})**{rating_str}{cuisine_str}{src_str}"
            )
        lines.append("")
        return lines

    def _render_directions(self, directions: dict, source: str, destination: str) -> list[str]:
        maps_url   = directions.get("maps_url") or (
            f"https://www.google.com/maps/dir/"
            f"{urllib.parse.quote(source)}/{urllib.parse.quote(destination)}"
        )
        lines = [
            "## 🧭 Getting There",
            f"**Route:** {directions.get('start_address', source)} → "
            f"{directions.get('end_address', destination)}",
            f"**Distance:** {directions.get('distance', 'N/A')}",
            f"**Duration:** {directions.get('duration', 'N/A')}",
            f"**[📍 Open in Google Maps]({maps_url})**",
        ]
        if directions.get("note"):
            lines.append(f"*{directions['note']}*")
        lines.append("")
        return lines

    def _render_bookings(self, bookings: list[dict], destination: str) -> list[str]:
        if not bookings:
            return []
        lines = ["## 🎫 Provisional Bookings", ""]
        for b in bookings:
            btype  = b.get("booking_type", "N/A").title()
            ref    = b.get("reference", "N/A")
            status = b.get("status", "N/A")
            lines.append(f"- **{btype}** — Ref: `{ref}` ({status})")
            details = b.get("details") or {}
            dest = details.get("name") or details.get("destination") or destination
            if dest and b.get("booking_type") == "hotel":
                dst_q = urllib.parse.quote(dest)
                lines.append(
                    f"  Finalize on: [Booking.com]"
                    f"(https://www.booking.com/searchresults.html?ss={dst_q})"
                )
        lines.append("")
        return lines

    def _render_sources(self, sources: list[dict]) -> list[str]:
        if not sources:
            return []
        lines = ["## 📎 Research Sources", ""]
        seen_urls: set[str] = set()
        for s in sources:
            url   = s.get("url", "")
            title = s.get("title", s.get("source", "Source"))
            src   = s.get("source", "")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            display = f"{title} ({src})" if src and src not in title else title
            lines.append(f"- [{display}]({url})")
        lines.append("")
        return lines
