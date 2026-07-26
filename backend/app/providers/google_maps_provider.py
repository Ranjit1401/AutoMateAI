"""
Real Google Maps Platform integration (Geocoding, Places Nearby Search,
Directions). Requires GOOGLE_MAPS_API_KEY with the corresponding APIs
enabled in the Google Cloud Console:
  - Geocoding API
  - Places API
  - Directions API
"""
from datetime import timedelta

import requests

from app.core.config import settings
from app.core.logging_config import get_logger
from app.providers.cache import TTLCache

logger = get_logger(__name__)

_GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
_PLACES_NEARBY_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
_DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json"


class GoogleMapsProvider:
    def __init__(self) -> None:
        self._cache = TTLCache(ttl=timedelta(hours=6))

    def _require_key(self) -> str:
        if not settings.GOOGLE_MAPS_API_KEY:
            raise RuntimeError("GOOGLE_MAPS_API_KEY is not configured.")
        return settings.GOOGLE_MAPS_API_KEY

    def geocode(self, address: str) -> dict:
        cache_key = f"geocode-{address}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        response = requests.get(
            _GEOCODE_URL,
            params={"address": address, "key": self._require_key()},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "OK" or not data.get("results"):
            raise RuntimeError(f"Geocoding failed for '{address}': {data.get('status')}")

        location = data["results"][0]["geometry"]["location"]
        result = {
            "formatted_address": data["results"][0]["formatted_address"],
            "lat": location["lat"],
            "lng": location["lng"],
        }
        self._cache.set(cache_key, result)
        return result

    def nearby_places(self, lat: float, lng: float, place_type: str, radius_m: int = 3000, keyword: str | None = None) -> list[dict]:
        cache_key = f"nearby-{lat}-{lng}-{place_type}-{radius_m}-{keyword}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        params = {
            "location": f"{lat},{lng}",
            "radius": radius_m,
            "type": place_type,
            "key": self._require_key(),
        }
        if keyword:
            params["keyword"] = keyword

        response = requests.get(_PLACES_NEARBY_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") not in ("OK", "ZERO_RESULTS"):
            raise RuntimeError(f"Places search failed: {data.get('status')} — {data.get('error_message', '')}")

        places = [
            {
                "name": place.get("name"),
                "address": place.get("vicinity"),
                "rating": place.get("rating"),
                "user_ratings_total": place.get("user_ratings_total"),
                "price_level": place.get("price_level"),
                "place_id": place.get("place_id"),
            }
            for place in data.get("results", [])
        ]
        self._cache.set(cache_key, places)
        return places

    def directions(self, origin: str, destination: str, mode: str = "driving") -> dict:
        cache_key = f"directions-{origin}-{destination}-{mode}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        response = requests.get(
            _DIRECTIONS_URL,
            params={"origin": origin, "destination": destination, "mode": mode, "key": self._require_key()},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "OK" or not data.get("routes"):
            raise RuntimeError(f"Directions failed: {data.get('status')}")

        leg = data["routes"][0]["legs"][0]
        result = {
            "distance": leg["distance"]["text"],
            "duration": leg["duration"]["text"],
            "start_address": leg["start_address"],
            "end_address": leg["end_address"],
            "steps": [
                {"instruction": step.get("html_instructions", ""), "distance": step["distance"]["text"]}
                for step in leg.get("steps", [])
            ],
        }
        self._cache.set(cache_key, result)
        return result


google_maps_provider = GoogleMapsProvider()
