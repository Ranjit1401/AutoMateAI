"""
ResearchAgent — upgraded from LLM-only to real web search via Tavily.

Flow:
  1. Run 3 targeted Tavily searches (attractions, food, travel tips).
  2. Collect all result URLs as real sources.
  3. Feed the combined snippets to the LLM to produce a structured
     DestinationResearch object — the LLM synthesises REAL data, not
     invented facts.
  4. If Tavily returns nothing (key missing / network error), fall back
     to the LLM-only path; if that also fails, use static fallback data.
"""
from app.agents.base_agent import BaseAgent
from app.agents.mixins import TravelExtractionMixin
from app.core.logging_config import get_logger
from app.providers.tavily_provider import tavily_provider
from app.schemas.research import DestinationResearch

logger = get_logger(__name__)


class ResearchAgent(BaseAgent, TravelExtractionMixin):
    """Researches a destination using live Tavily web search results."""

    def __init__(self):
        super().__init__()
        self._research_parser = self.llm.with_structured_output(DestinationResearch)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_context(destination: str) -> tuple[str, list[dict]]:
        """
        Run 3 targeted Tavily searches and return (context_text, sources).
        sources is a list of {title, url, source} dicts for every result found.
        """
        queries = [
            f"top tourist attractions places to visit in {destination} 2024",
            f"best local food restaurants must try dishes in {destination}",
            f"travel tips best time to visit {destination} India",
        ]

        all_sources: list[dict] = []
        snippets: list[str] = []

        for query in queries:
            results = tavily_provider.search(query=query, max_results=5, search_depth="advanced")
            for r in results:
                snippets.append(f"[{r['source']}] {r['title']}: {r['content'][:400]}")
                all_sources.append({
                    "title":  r["title"],
                    "url":    r["url"],
                    "source": r["source"],
                })

        context = "\n\n".join(snippets)
        return context, all_sources

    def _research_with_tavily(self, destination: str) -> tuple[DestinationResearch, list[dict]]:
        """Search Tavily → synthesise with LLM → return (structured, sources)."""
        context, sources = self._build_context(destination)

        if not context.strip():
            # Tavily returned nothing — fall through to LLM-only path
            raise RuntimeError("Tavily returned no results")

        prompt = (
            f"You are a travel research assistant. Based ONLY on the following real web "
            f"search results about {destination}, extract structured travel information.\n\n"
            f"Search Results:\n{context}\n\n"
            f"Extract for {destination}:\n"
            "- A 2-sentence summary of what makes this destination worth visiting\n"
            "- 4-6 specific must-visit places or attractions (use real names from the results)\n"
            "- 3-5 local dishes or food experiences (use real names from the results)\n"
            "- Best months/season to visit\n\n"
            "Use ONLY information from the search results. Do NOT invent places or dishes."
        )
        result = self._research_parser.invoke(prompt)
        return result, sources

    def _research_llm_only(self, destination: str) -> DestinationResearch:
        """LLM-only fallback (no Tavily context). Still better than static data."""
        prompt = (
            "You are a travel research assistant. Provide accurate, specific "
            f"information about visiting {destination}.\n"
            "Only include real places and dishes associated with this destination."
        )
        return self._research_parser.invoke(prompt)

    def research(self, destination: str) -> tuple[DestinationResearch, list[dict]]:
        """
        Returns (DestinationResearch, sources_list).
        sources_list contains {title, url, source} dicts from Tavily results.
        """
        # --- Try Tavily + LLM synthesis first ---
        try:
            return self._research_with_tavily(destination)
        except Exception as tavily_exc:  # noqa: BLE001
            logger.warning(
                "Tavily-based research failed (%s); falling back to LLM-only.", tavily_exc
            )

        # --- Try LLM-only ---
        try:
            return self._research_llm_only(destination), []
        except Exception:  # noqa: BLE001
            logger.exception("Research LLM call also failed; using static fallback data.")
            from app.agents.fallback_data import fallback_destination_research
            return fallback_destination_research(destination), []

    # ------------------------------------------------------------------
    # Agent interface
    # ------------------------------------------------------------------

    def execute(self, action: str, state: dict) -> dict:
        travel = self.extract_travel(state["user_input"])
        destination = travel.destination

        research, sources = self.research(destination)

        return {
            "action": action,
            "research": {
                "destination":  destination,
                "best_time":    research.best_time_to_visit,
                "top_places":   research.top_places,
                "local_food":   research.local_food,
                "summary":      research.summary,
                # Real Tavily sources — eliminates "Source: None"
                "sources":      sources,
                "tool_used":    "Tavily Search" if sources else "LLM",
            },
        }
