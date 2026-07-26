"""
MapsTool — upgraded to always generate clickable Google Maps links.

Behaviour:
  1. If GOOGLE_MAPS_API_KEY is set → attempt real Directions API call.
  2. Always include a Google Maps search/directions URL (no API key needed).
  3. Fallback to static directions text if API call fails.

This ensures every response includes a usable Google Maps link even
without a Maps API key.
"""
import urllib.parse

from app.tools.base import BaseTool


def _maps_directions_url(origin: str, destination: str, mode: str = "driving") -> str:
    """Generate a Google Maps directions URL (no API key required)."""
    o = urllib.parse.quote(origin)
    d = urllib.parse.quote(destination)
    return f"https://www.google.com/maps/dir/{o}/{d}/?travelmode={mode}"


def _maps_search_url(place: str) -> str:
    """Generate a Google Maps search URL for a single place."""
    q = urllib.parse.quote(place)
    return f"https://www.google.com/maps/search/{q}"


class MapsTool(BaseTool):
    name = "maps"
    description = (
        "Gets directions (distance/duration) between two locations and generates "
        "a clickable Google Maps link. Works without a Maps API key."
    )

    def execute(self, origin: str, destination: str, mode: str = "driving") -> dict:
        from app.agents.fallback_data import fallback_directions  # noqa: PLC0415

        maps_url = _maps_directions_url(origin, destination, mode)

        # --- Attempt live Directions API ---
        try:
            from app.providers.google_maps_provider import google_maps_provider

            result = google_maps_provider.directions(
                origin=origin, destination=destination, mode=mode
            )
            # Inject the clickable URL into the live result
            result["maps_url"] = maps_url
            result["search_url"] = _maps_search_url(destination)
            return result
        except Exception:  # noqa: BLE001
            pass

        # --- Fallback directions + always-valid maps URL ---
        fallback = fallback_directions(origin, destination)
        fallback["maps_url"]    = maps_url
        fallback["search_url"]  = _maps_search_url(destination)
        fallback["note"]        = "Directions are approximate. Click the link for exact route."
        return fallback


def attraction_maps_url(attraction: str, destination: str) -> str:
    """
    Public helper — generate a Google Maps search URL for a specific
    attraction in a destination. Used by the response agent to add
    maps links to every place in the itinerary.
    """
    return _maps_search_url(f"{attraction}, {destination}")
