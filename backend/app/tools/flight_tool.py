"""
FlightTool — upgraded to generate real Google Flights search URLs.

Priority order:
  1. SerpAPI Google Flights (live data) — if key is present and returns results.
  2. Dynamic Google Flights search URL + MakeMyTrip URL — always works, no API needed.
  3. Static fallback demo data — only if caller explicitly falls through.

The key change: when SerpAPI fails or returns nothing, we NO LONGER return
hardcoded fake airline/flight data. Instead we return real search links that
the user can click to see actual prices.
"""
import urllib.parse
from datetime import date, timedelta

from app.tools.base import BaseTool

# Extended IATA airport code map
AIRPORTS: dict[str, str] = {
    "Mumbai":     "BOM",
    "Goa":        "GOI",
    "Delhi":      "DEL",
    "Bangalore":  "BLR",
    "Bengaluru":  "BLR",
    "Hyderabad":  "HYD",
    "Chennai":    "MAA",
    "Kolkata":    "CCU",
    "Pune":       "PNQ",
    "Ahmedabad":  "AMD",
    "Jaipur":     "JAI",
    "Kochi":      "COK",
    "Guwahati":   "GAU",
    "Lucknow":    "LKO",
    "Varanasi":   "VNS",
    "Amritsar":   "ATQ",
    "Udaipur":    "UDR",
    "Srinagar":   "SXR",
    "Manali":     None,     # no commercial airport — road/bus only
    "Shimla":     "SLV",
    "Andaman":    "IXZ",
    "Port Blair": "IXZ",
}


def _google_flights_url(source: str, destination: str, travel_date: str) -> str:
    """Generate a direct Google Flights search URL for the given route."""
    src_enc = urllib.parse.quote(source)
    dst_enc = urllib.parse.quote(destination)
    return (
        f"https://www.google.com/travel/flights?q="
        f"Flights+from+{src_enc}+to+{dst_enc}+on+{travel_date}"
    )


def _makemytrip_url(src_code: str | None, dst_code: str | None, travel_date: str) -> str:
    """Generate a MakeMyTrip search URL using IATA codes when available."""
    if src_code and dst_code:
        # MakeMyTrip wants date in the DDMMYYYY format in the itinerary param
        try:
            d = date.fromisoformat(travel_date)
            mmt_date = d.strftime("%d%m%Y")
        except ValueError:
            mmt_date = travel_date.replace("-", "")
        return (
            f"https://www.makemytrip.com/flight/search?"
            f"itinerary={src_code}-{dst_code}-{mmt_date}"
            f"&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E"
        )
    return f"https://www.makemytrip.com/flights/"


def _ixigo_url(source: str, destination: str, travel_date: str) -> str:
    src_enc = urllib.parse.quote(source)
    dst_enc = urllib.parse.quote(destination)
    return f"https://www.ixigo.com/search/result/flight?from={src_enc}&to={dst_enc}&date={travel_date}&adults=1&class=e"


def _search_links(source: str, destination: str) -> list[dict]:
    """
    Return a list of real flight search link entries.
    These are ALWAYS valid — no API key required.
    """
    travel_date = (date.today() + timedelta(days=30)).isoformat()
    src_code = AIRPORTS.get(source)
    dst_code = AIRPORTS.get(destination)

    links = [
        {
            "airline":       "Google Flights",
            "type":          "search_link",
            "search_url":    _google_flights_url(source, destination, travel_date),
            "description":   f"Search all flights from {source} to {destination} on Google Flights",
            "departure":     travel_date,
            "price":         "Check live prices →",
        },
        {
            "airline":       "MakeMyTrip",
            "type":          "search_link",
            "search_url":    _makemytrip_url(src_code, dst_code, travel_date),
            "description":   f"Search flights from {source} to {destination} on MakeMyTrip",
            "departure":     travel_date,
            "price":         "Check live prices →",
        },
        {
            "airline":       "ixigo",
            "type":          "search_link",
            "search_url":    _ixigo_url(source, destination, travel_date),
            "description":   f"Search flights from {source} to {destination} on ixigo",
            "departure":     travel_date,
            "price":         "Check live prices →",
        },
    ]

    # If destination has no commercial airport, add a note
    if dst_code is None:
        links.insert(0, {
            "airline":    "Note",
            "type":       "info",
            "description": f"{destination} has no direct commercial flight connection. "
                           f"Fly to the nearest major airport and continue by road.",
            "search_url": _google_flights_url(source, "Delhi", travel_date),
        })

    return links


class FlightTool(BaseTool):
    name = "flight"
    description = (
        "Returns live flight offers or real Google Flights / MakeMyTrip search links "
        "between two cities. Never returns fake/invented flight data."
    )

    def execute(self, source: str, destination: str) -> list[dict]:
        from app.agents.fallback_data import fallback_flights  # noqa: PLC0415

        departure = (date.today() + timedelta(days=30)).isoformat()

        # --- Attempt 1: SerpAPI live data (paid plan) ---
        src_code = AIRPORTS.get(source)
        dst_code = AIRPORTS.get(destination)

        if src_code and dst_code:
            try:
                from app.providers.serpapi_provider import serp_provider

                data = serp_provider.search_flights(
                    departure_id=src_code,
                    arrival_id=dst_code,
                    outbound_date=departure,
                )
                all_flights = data.get("best_flights", []) + data.get("other_flights", [])
                if all_flights:
                    flights = []
                    for offer in all_flights[:5]:
                        seg = offer["flights"][0]
                        flights.append({
                            "airline":       seg["airline"],
                            "flight_number": seg["flight_number"],
                            "departure":     seg["departure_airport"]["time"],
                            "arrival":       seg["arrival_airport"]["time"],
                            "duration":      offer["total_duration"],
                            "price":         offer.get("price", "See link"),
                            "type":          "live",
                            "source_url":    _google_flights_url(source, destination, departure),
                        })
                    return flights
            except Exception:  # noqa: BLE001
                pass  # fall through to search links

        # --- Attempt 2: Real search links (always works, no API key needed) ---
        return _search_links(source, destination)
