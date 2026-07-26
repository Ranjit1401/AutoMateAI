"""
SerpApi wrapper (Google Flights / Google Hotels). Lazily initialized so a
missing API key doesn't crash the whole app at import time — the previous
version raised ValueError at module load, which meant nothing in
`app.tools` could even be imported without SERPAPI_API_KEY set. Now the
error only surfaces when a flight/hotel search is actually attempted.
"""
from datetime import datetime, timedelta

from serpapi import GoogleSearch

from app.core.config import settings
from app.core.logging_config import get_logger
from app.providers.cache import TTLCache

logger = get_logger(__name__)


class SerpAPIProvider:
    def __init__(self) -> None:
        self._cache = TTLCache(ttl=timedelta(hours=1))

    def _require_key(self) -> str:
        if not settings.SERPAPI_API_KEY:
            raise RuntimeError("SERPAPI_API_KEY is not configured.")
        return settings.SERPAPI_API_KEY

    def search_flights(self, departure_id: str, arrival_id: str, outbound_date: str) -> dict:
        outbound = datetime.strptime(outbound_date, "%Y-%m-%d")
        return_date = (outbound + timedelta(days=5)).strftime("%Y-%m-%d")

        cache_key = f"flight-{departure_id}-{arrival_id}-{outbound_date}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            logger.debug("Flight cache hit: %s", cache_key)
            return cached

        params = {
            "engine": "google_flights",
            "departure_id": departure_id,
            "arrival_id": arrival_id,
            "outbound_date": outbound_date,
            "return_date": return_date,
            "currency": "INR",
            "hl": "en",
            "api_key": self._require_key(),
        }

        results = GoogleSearch(params).get_dict()
        self._cache.set(cache_key, results)
        return results

    def search_hotels(self, location: str, check_in_date: str | None = None, check_out_date: str | None = None) -> dict:
        cache_key = f"hotel-{location}-{check_in_date}-{check_out_date}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            logger.debug("Hotel cache hit: %s", cache_key)
            return cached

        params = {
            "engine": "google_hotels",
            "q": location,
            "currency": "INR",
            "hl": "en",
            "api_key": self._require_key(),
        }
        if check_in_date:
            params["check_in_date"] = check_in_date
        if check_out_date:
            params["check_out_date"] = check_out_date

        results = GoogleSearch(params).get_dict()
        self._cache.set(cache_key, results)
        return results

    def search_web(self, query: str) -> dict:
        cache_key = f"web-{query}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            logger.debug("Web search cache hit: %s", cache_key)
            return cached

        params = {"engine": "google", "q": query, "hl": "en", "api_key": self._require_key()}
        results = GoogleSearch(params).get_dict()
        self._cache.set(cache_key, results)
        return results


serp_provider = SerpAPIProvider()
