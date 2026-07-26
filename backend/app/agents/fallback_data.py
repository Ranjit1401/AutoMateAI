"""
Deterministic fallback/demo data.

Every LLM call and every paid external API call in this project can fail
for reasons that have nothing to do with the user's request: a missing
GROQ_API_KEY, an expired SerpApi/Google Maps/OpenWeather key, a rate limit,
or no network access on the demo machine's wifi.

Rather than let any of those bubble up as a raised exception (which turns
into a blank/error card in the UI), each call site catches the failure and
falls back to the realistic, deterministic data generated here. This file
is the single place that logic lives, so it's easy to audit/replace once
real keys are always available.
"""
from __future__ import annotations

import re
from datetime import date, timedelta

# ---------------------------------------------------------------------------
# Travel-detail extraction fallback (used by TravelExtractionMixin)
# ---------------------------------------------------------------------------

_CITY_ALIASES: dict[str, str] = {
    "goa": "Goa",
    "mumbai": "Mumbai",
    "delhi": "Delhi",
    "new delhi": "Delhi",
    "bangalore": "Bangalore",
    "bengaluru": "Bangalore",
    "hyderabad": "Hyderabad",
    "chennai": "Chennai",
    "kolkata": "Kolkata",
    "jaipur": "Jaipur",
    "kerala": "Kerala",
    "manali": "Manali",
    "shimla": "Shimla",
    "udaipur": "Udaipur",
    "pune": "Pune",
    "agra": "Agra",
    "varanasi": "Varanasi",
    "rishikesh": "Rishikesh",
    "kashmir": "Kashmir",
    "andaman": "Andaman",
}


def _find_city(text: str) -> str | None:
    lowered = text.lower()
    for key, name in _CITY_ALIASES.items():
        if re.search(rf"\b{re.escape(key)}\b", lowered):
            return name
    return None


def fallback_travel_input(user_input: str):
    """Regex-based best-effort extraction, used only when the LLM call
    fails. Always returns a fully-populated, schema-valid TravelInput so
    downstream tools never receive None/blank fields."""
    from app.schemas.travel import TravelInput

    lowered = user_input.lower()
    destination = _find_city(user_input) or "Goa"
    source = "Mumbai" if destination != "Mumbai" else "Delhi"

    budget_match = re.search(r"(?:₹|rs\.?|inr)\s?([\d,]{3,})", lowered)
    budget = int(budget_match.group(1).replace(",", "")) if budget_match else 30000

    days_match = re.search(r"(\d+)\s*[-\s]?\s*day", lowered)
    days = int(days_match.group(1)) if days_match else 5

    travellers_match = re.search(r"(\d+)\s*(?:people|travellers|travelers|persons|pax|adults)", lowered)
    travellers = int(travellers_match.group(1)) if travellers_match else 1

    start = date.today() + timedelta(days=30)
    end = start + timedelta(days=max(days - 1, 1))

    return TravelInput(
        source=source,
        destination=destination,
        budget=budget,
        start_date=start.isoformat(),
        end_date=end.isoformat(),
        travellers=travellers,
    )


# ---------------------------------------------------------------------------
# Router / Planner fallback
# ---------------------------------------------------------------------------

_TRAVEL_HINTS = (
    "trip", "travel", "vacation", "holiday", "flight", "hotel", "itinerary",
    "visit", "tour", "goa", "budget",
)


def fallback_router_response():
    from app.schemas.router import RouterResponse

    return RouterResponse(task_type="travel", reason="Fallback classification (LLM unavailable).")


def fallback_planner_response():
    from app.schemas.planner import PlannerResponse

    steps = [
        "Check weather and available flights/hotels for the trip",
        "Research top attractions and local food for the destination",
        "Build a day-by-day itinerary for the trip",
        "Estimate the total budget and cost breakdown",
        "Find recommended restaurants near the destination",
        "Get driving directions/route to the destination",
        "Reserve the best flight and hotel option",
    ]
    return PlannerResponse(
        goal="Plan the trip end-to-end (weather, flights, hotels, itinerary, budget, dining, directions, booking).",
        estimated_complexity="medium",
        required_agents=["travel", "research", "itinerary", "budget", "restaurant", "maps", "booking"],
        steps=steps,
    )


# ---------------------------------------------------------------------------
# Research / Itinerary fallback
# ---------------------------------------------------------------------------

def fallback_destination_research(destination: str):
    from app.schemas.research import DestinationResearch

    return DestinationResearch(
        summary=f"{destination} is a popular travel destination known for its mix of relaxation and culture.",
        top_places=[
            f"{destination} main beachfront / city center",
            f"{destination} old town / heritage quarter",
            f"Popular local market in {destination}",
            f"Scenic viewpoint near {destination}",
        ],
        local_food=["Local thali", "Regional seafood/vegetarian specialty", "Street food favorites"],
        best_time_to_visit="November to February (cooler, pleasant weather)",
    )


def fallback_itinerary_plan(nights: int):
    from app.schemas.itinerary import ItineraryDay, ItineraryPlan

    themes = [
        "Arrival & relaxed exploration",
        "Sightseeing & local landmarks",
        "Culture, markets & local cuisine",
        "Nature, viewpoints & leisure",
        "Free day / optional activities",
        "Day trip to nearby attraction",
        "Departure & last-minute shopping",
    ]
    days = []
    for i in range(max(nights, 1)):
        theme = themes[i % len(themes)]
        days.append(
            ItineraryDay(
                day=i + 1,
                theme=theme,
                activities=[
                    "Breakfast at hotel",
                    f"Morning: {theme.split(' &')[0].lower()}",
                    "Afternoon: local lunch + leisure time",
                    "Evening: sunset spot / local market",
                ],
            )
        )
    return ItineraryPlan(days=days)


# ---------------------------------------------------------------------------
# Memory extraction fallback
# ---------------------------------------------------------------------------

def fallback_memory_extraction():
    from app.schemas.memory_extraction import MemoryExtraction

    return MemoryExtraction(has_durable_fact=False, fact=None, category="general")


# ---------------------------------------------------------------------------
# Tool-level demo data (flights / hotels / weather / directions / restaurants)
# ---------------------------------------------------------------------------

def fallback_flights(source: str, destination: str) -> list[dict]:
    departure = (date.today() + timedelta(days=30)).isoformat() + "T09:15:00"
    arrival = (date.today() + timedelta(days=30)).isoformat() + "T11:05:00"
    airlines = [
        ("IndiGo", "6E-234", 4899),
        ("Air India", "AI-665", 5750),
        ("SpiceJet", "SG-112", 4550),
    ]
    return [
        {
            "airline": name,
            "flight_number": num,
            "departure": departure,
            "arrival": arrival,
            "duration": "1 hr 50 min",
            "price": price,
        }
        for name, num, price in airlines
    ]


def fallback_hotels(destination: str) -> list[dict]:
    return [
        {"name": f"{destination} Beach Resort & Spa", "price": 4500, "rating": 4.5},
        {"name": f"Hotel {destination} Grand", "price": 3200, "rating": 4.2},
        {"name": f"{destination} Budget Inn", "price": 1800, "rating": 3.9},
    ]


def fallback_weather(city: str) -> dict:
    return {"city": city, "temperature": 29, "condition": "Sunny", "humidity": 65, "wind_speed": 3.4}


def fallback_directions(origin: str, destination: str) -> dict:
    return {
        "distance": "590 km",
        "duration": "10 hr 30 min",
        "start_address": origin,
        "end_address": destination,
        "steps": [{"instruction": f"Head out of {origin} towards {destination}", "distance": "590 km"}],
    }


def fallback_restaurants(destination: str) -> list[dict]:
    return [
        {"name": f"{destination} Spice Kitchen", "address": f"Main Road, {destination}", "rating": 4.6, "user_ratings_total": 1200, "price_level": 2},
        {"name": f"Seaside Shack, {destination}", "address": f"Beach Road, {destination}", "rating": 4.4, "user_ratings_total": 850, "price_level": 2},
        {"name": f"{destination} Local Bites", "address": f"Market Street, {destination}", "rating": 4.2, "user_ratings_total": 400, "price_level": 1},
    ]


# ---------------------------------------------------------------------------
# Booking links (used by the response agent to build clickable booking URLs)
# ---------------------------------------------------------------------------

def booking_links(source: str, destination: str) -> dict:
    import urllib.parse

    src_q = urllib.parse.quote(source or "Mumbai")
    dst_q = urllib.parse.quote(destination)
    date_q = (date.today() + timedelta(days=30)).isoformat()

    return {
        "flights": {
            "Google Flights": f"https://www.google.com/travel/flights?q=Flights%20from%20{src_q}%20to%20{dst_q}%20on%20{date_q}",
            "MakeMyTrip": f"https://www.makemytrip.com/flight/search?itinerary={src_q}-{dst_q}-{date_q}&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E",
        },
        "hotels": {
            "Booking.com": f"https://www.booking.com/searchresults.html?ss={dst_q}",
            "Agoda": f"https://www.agoda.com/search?city={dst_q}",
            "MakeMyTrip": f"https://www.makemytrip.com/hotels/hotel-listing/?city={dst_q}",
        },
    }
