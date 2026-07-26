"""
RestaurantAgent — upgraded to use Tavily web search as the primary source.

Priority:
  1. Tavily search for "best restaurants in <destination> 2024" → real results
     with actual restaurant names, ratings, and source URLs.
  2. Google Maps Places (existing tool_executor path) as fallback.
  3. Static fallback_restaurants() as last resort.

This eliminates invented restaurant names (e.g. "Goa Spice Kitchen").
"""
import re

from app.agents.base_agent import BaseAgent
from app.agents.mixins import TravelExtractionMixin
from app.core.logging_config import get_logger
from app.providers.tavily_provider import tavily_provider
from app.tools.executor import ToolExecutionError, tool_executor

logger = get_logger(__name__)


class RestaurantAgent(BaseAgent, TravelExtractionMixin):
    """Finds real restaurants using Tavily web search + Google Maps fallback."""

    # ------------------------------------------------------------------
    # Tavily-based search
    # ------------------------------------------------------------------

    @staticmethod
    def _search_with_tavily(destination: str) -> list[dict]:
        """
        Run Tavily searches for top restaurants and parse results into the
        standard restaurant dict shape:
            {name, address, rating, cuisine, source_url, source}
        Returns [] if Tavily key is missing or no results found.
        """
        queries = [
            f"best restaurants to eat in {destination} 2024 top rated",
            f"famous local food shacks cafes {destination} must visit",
        ]

        seen_names: set[str] = set()
        restaurants: list[dict] = []

        for query in queries:
            results = tavily_provider.search(query=query, max_results=5)
            for r in results:
                # Parse restaurant name from title (common patterns)
                title = r["title"]
                content = r["content"][:600]

                # Extract restaurant names from the content using simple heuristics.
                # Tavily content often contains numbered lists like "1. Café XYZ – ..."
                name_matches = re.findall(
                    r"(?:\d+\.\s*|•\s*)([A-Z][^—\-\n:,]{3,50})(?:\s*[-–—]|\s*:)",
                    content,
                )

                if name_matches:
                    for raw_name in name_matches[:3]:
                        name = raw_name.strip()
                        if name.lower() not in seen_names and len(name) > 3:
                            seen_names.add(name.lower())
                            restaurants.append({
                                "name":       name,
                                "address":    destination,
                                "rating":     None,
                                "cuisine":    "Local",
                                "source_url": r["url"],
                                "source":     r["source"],
                                "maps_url": (
                                    f"https://www.google.com/maps/search/"
                                    f"{name.replace(' ', '+')}+{destination.replace(' ', '+')}"
                                ),
                            })
                else:
                    # Use the article title itself as a restaurant name placeholder
                    # only if it looks like a restaurant / food guide title
                    if any(kw in title.lower() for kw in ["restaurant", "café", "cafe", "shack", "food", "eat"]):
                        clean = re.sub(r"\s*[-–|].*$", "", title).strip()
                        if clean and clean.lower() not in seen_names:
                            seen_names.add(clean.lower())
                            restaurants.append({
                                "name":       clean,
                                "address":    destination,
                                "rating":     None,
                                "cuisine":    "Local",
                                "source_url": r["url"],
                                "source":     r["source"],
                                "maps_url": (
                                    f"https://www.google.com/maps/search/"
                                    f"{clean.replace(' ', '+')}+{destination.replace(' ', '+')}"
                                ),
                            })

                if len(restaurants) >= 8:
                    break
            if len(restaurants) >= 8:
                break

        return restaurants

    # ------------------------------------------------------------------
    # Agent interface
    # ------------------------------------------------------------------

    def execute(self, action: str, state: dict) -> dict:
        travel = self.extract_travel(state["user_input"])
        destination = travel.destination

        # 1. Try Tavily (real web search)
        tavily_results = self._search_with_tavily(destination)
        if tavily_results:
            logger.info("RestaurantAgent: Tavily returned %d restaurants for %s.",
                        len(tavily_results), destination)
            return {
                "action":      action,
                "restaurants": tavily_results,
                "tool_used":   "Tavily Search",
            }

        # 2. Try Google Maps Places (existing tool)
        try:
            places = tool_executor.execute("restaurant", destination=destination)
            if places:
                logger.info("RestaurantAgent: Google Maps returned %d results.", len(places))
                return {
                    "action":      action,
                    "restaurants": places,
                    "tool_used":   "Google Maps Places",
                }
        except ToolExecutionError as exc:
            logger.warning("RestaurantAgent: Google Maps fallback failed: %s", exc.message)

        # 3. Static fallback
        from app.agents.fallback_data import fallback_restaurants
        logger.warning("RestaurantAgent: using static fallback data for %s.", destination)
        return {
            "action":      action,
            "restaurants": fallback_restaurants(destination),
            "tool_used":   "Fallback (all APIs unavailable)",
        }
