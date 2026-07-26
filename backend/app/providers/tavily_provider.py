"""
Tavily Search API provider.

Tavily is purpose-built for AI agents — it returns curated, cited web
results with full content snippets and source URLs, making it ideal for
replacing LLM hallucination with real, verifiable information.

Get a free API key at https://app.tavily.com
"""
from datetime import timedelta

import requests

from app.core.config import settings
from app.core.logging_config import get_logger
from app.providers.cache import TTLCache

logger = get_logger(__name__)

TAVILY_SEARCH_URL = "https://api.tavily.com/search"


class TavilyProvider:
    """Wraps the Tavily Search REST API with caching and graceful degradation."""

    def __init__(self) -> None:
        self._cache = TTLCache(ttl=timedelta(hours=2))

    def _require_key(self) -> str:
        if not settings.TAVILY_API_KEY:
            raise RuntimeError("TAVILY_API_KEY is not configured.")
        return settings.TAVILY_API_KEY

    def search(
        self,
        query: str,
        max_results: int = 6,
        search_depth: str = "advanced",
        include_domains: list[str] | None = None,
    ) -> list[dict]:
        """
        Execute a Tavily search and return a list of result dicts:
            {
                "title":   str,
                "url":     str,
                "content": str,   # 200-500 word snippet extracted by Tavily
                "source":  str,   # domain name, e.g. "tripadvisor.com"
                "score":   float, # Tavily relevance score
            }

        Returns an empty list (not an exception) when the API key is missing
        or any network/API error occurs — callers must handle [] as a signal
        to use fallback data.
        """
        cache_key = f"tavily-{query}-{max_results}-{search_depth}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            logger.debug("Tavily cache hit: %s", cache_key)
            return cached

        try:
            api_key = self._require_key()
        except RuntimeError:
            logger.warning("TAVILY_API_KEY not set — skipping web search.")
            return []

        payload: dict = {
            "api_key": api_key,
            "query": query,
            "max_results": max_results,
            "search_depth": search_depth,
            "include_answer": False,
        }
        if include_domains:
            payload["include_domains"] = include_domains

        try:
            response = requests.post(TAVILY_SEARCH_URL, json=payload, timeout=15)
            response.raise_for_status()
            data = response.json()

            results: list[dict] = []
            for r in data.get("results", []):
                url = r.get("url", "")
                # Extract domain for the "source" field
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(url).netloc.replace("www.", "")
                except Exception:
                    domain = url

                results.append(
                    {
                        "title": r.get("title", ""),
                        "url": url,
                        "content": r.get("content", ""),
                        "source": domain,
                        "score": r.get("score", 0.0),
                    }
                )

            self._cache.set(cache_key, results)
            logger.info("Tavily search '%s' returned %d results.", query, len(results))
            return results

        except requests.RequestException as exc:
            logger.error("Tavily API request failed for query %r: %s", query, exc)
            return []
        except Exception as exc:  # noqa: BLE001
            logger.error("Tavily unexpected error for query %r: %s", query, exc)
            return []


# Module-level singleton — matches the pattern used by serpapi_provider.py
tavily_provider = TavilyProvider()
