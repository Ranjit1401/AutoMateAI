"""
Web search tool — performs a general Google search via SerpAPI.
Returns the top organic results (title, snippet, link).
"""
import logging

from app.providers.serpapi_provider import serp_provider
from app.tools.base import BaseTool

logger = logging.getLogger(__name__)


class SearchTool(BaseTool):

    name = "search"
    description = "Performs a web search and returns the top results."

    def execute(self, query: str, num_results: int = 5) -> list[dict]:
        try:
            raw = serp_provider.search_places(query)  # reuses the generic search method
            organic = raw.get("organic_results", [])

            results: list[dict] = []
            for r in organic[:num_results]:
                results.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("snippet", ""),
                    "link": r.get("link", ""),
                    "source": r.get("source", ""),
                })
            return results

        except Exception as exc:
            logger.error("SearchTool error for query %r: %s", query, exc)
            return []
