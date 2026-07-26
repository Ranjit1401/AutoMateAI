"""
HotelTool — upgraded to generate real hotel search links.

Priority order:
  1. SerpAPI Google Hotels (live data) — if key is present and returns results.
  2. Real Booking.com / Agoda / Google Hotels search URLs — always works.
  3. Static fallback — only if this class is explicitly bypassed.

The key change: when SerpAPI fails, we NO LONGER return fake hotel names.
Instead, we return real search links the user can click.
"""
import urllib.parse
from datetime import date, timedelta

from app.tools.base import BaseTool


def _hotel_search_links(destination: str) -> list[dict]:
    """
    Generate real hotel booking search URLs for the destination.
    These are ALWAYS valid — no API key required.
    """
    dst_q = urllib.parse.quote(destination)
    check_in  = (date.today() + timedelta(days=30)).isoformat()
    check_out = (date.today() + timedelta(days=35)).isoformat()

    return [
        {
            "name":        "Search on Booking.com",
            "type":        "search_link",
            "url":         f"https://www.booking.com/searchresults.html?ss={dst_q}&checkin={check_in}&checkout={check_out}",
            "rating":      None,
            "price":       "Check live prices →",
            "description": f"Browse all available hotels in {destination} on Booking.com",
        },
        {
            "name":        "Search on Agoda",
            "type":        "search_link",
            "url":         f"https://www.agoda.com/search?city={dst_q}&checkIn={check_in}&checkOut={check_out}",
            "rating":      None,
            "price":       "Check live prices →",
            "description": f"Browse all available hotels in {destination} on Agoda",
        },
        {
            "name":        "Search on Google Hotels",
            "type":        "search_link",
            "url":         (
                f"https://www.google.com/travel/hotels?q=Hotels+in+{dst_q}"
                f"&dates={check_in},{check_out}"
            ),
            "rating":      None,
            "price":       "Check live prices →",
            "description": f"Browse hotels in {destination} on Google Hotels",
        },
        {
            "name":        "Search on MakeMyTrip",
            "type":        "search_link",
            "url":         f"https://www.makemytrip.com/hotels/hotel-listing/?city={dst_q}&chkIn={check_in}&chkOut={check_out}",
            "rating":      None,
            "price":       "Check live prices →",
            "description": f"Browse hotels in {destination} on MakeMyTrip",
        },
    ]


class HotelTool(BaseTool):
    name = "hotel"
    description = (
        "Returns live hotel listings or real Booking.com / Google Hotels search links "
        "for a destination. Never returns fake/invented hotel names."
    )

    def execute(self, destination: str) -> list[dict]:
        from app.agents.fallback_data import fallback_hotels  # noqa: PLC0415

        # --- Attempt 1: SerpAPI live data ---
        try:
            from app.providers.serpapi_provider import serp_provider

            data = serp_provider.search_hotels(destination)
            hotels = []
            for hotel in data.get("properties", [])[:5]:
                price = hotel.get("rate_per_night", {}).get("lowest")
                name = hotel.get("name")
                if not price or not name:
                    continue
                hotels.append({
                    "name":   name,
                    "price":  price,
                    "rating": hotel.get("overall_rating") or 4.0,
                    "type":   "live",
                    "url":    (
                        f"https://www.booking.com/searchresults.html?"
                        f"ss={urllib.parse.quote(destination)}"
                    ),
                })
            if hotels:
                return hotels
        except Exception:  # noqa: BLE001
            pass  # fall through to search links

        # --- Attempt 2: Real booking search links ---
        return _hotel_search_links(destination)
