"""
Web search tool — performs a real web search via Tavily Search API.

Tavily is purpose-built for AI agents and returns cited results with
real source URLs instead of generic snippets. Replaces the previous
SerpAPI-based implementation that produced "Source: None".
"""
import logging

from app.providers.tavily_provider import tavily_provider
from app.tools.base import BaseTool

logger = logging.getLogger(__name__)


class SearchTool(BaseTool):

    name = "search"
    description = "Performs a real web search via Tavily and returns cited results with source URLs."

    def execute(self, query: str, num_results: int = 6) -> list[dict]:
        try:
            results = tavily_provider.search(query=query, max_results=num_results)
            # Normalise to the same shape the rest of the codebase expects
            return [
                {
                    "title":   r["title"],
                    "snippet": r["content"],          # Tavily "content" = rich snippet
                    "link":    r["url"],
                    "source":  r["source"],           # real domain, never empty
                    "score":   r.get("score", 0.0),
                }
                for r in results
            ]
        except Exception as exc:
            logger.error("SearchTool error for query %r: %s", query, exc)
            return []
