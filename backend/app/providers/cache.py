"""Small in-process TTL cache shared by external-API providers, so repeated
identical lookups (same city weather, same flight search) within the TTL
window don't re-hit paid third-party APIs. Consolidated from the duplicate
cache implementation that used to live inline inside serpapi_provider.py."""
from datetime import datetime, timedelta
from typing import Any


class TTLCache:
    def __init__(self, ttl: timedelta = timedelta(hours=1)):
        self._ttl = ttl
        self._store: dict[str, tuple[Any, datetime]] = {}

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry is None:
            return None
        value, timestamp = entry
        if datetime.now() - timestamp > self._ttl:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any) -> None:
        self._store[key] = (value, datetime.now())
