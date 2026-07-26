"""Shared behavior for agents that need structured travel details pulled
out of the raw user message. Previously this exact extraction logic was
copy-pasted into both TravelAgent and ResearchAgent; now every agent that
needs it reuses one implementation."""
from app.core.logging_config import get_logger
from app.prompts.travel_prompt import TRAVEL_PROMPT
from app.schemas.travel import TravelInput

logger = get_logger(__name__)


class TravelExtractionMixin:
    """Mixin classes assume `self.llm` is provided by BaseAgent."""

    def _travel_parser(self):
        if not hasattr(self, "_cached_travel_parser"):
            self._cached_travel_parser = self.llm.with_structured_output(TravelInput)
        return self._cached_travel_parser

    def extract_travel(self, user_input: str) -> TravelInput:
        """Falls back to regex-based extraction (app/agents/fallback_data.py)
        if the LLM call fails for any reason (missing GROQ_API_KEY, network
        issue, rate limit) - the demo must never crash for this reason."""
        prompt = f"{TRAVEL_PROMPT}\n\nUser Request:\n{user_input}"
        try:
            return self._travel_parser().invoke(prompt)
        except Exception:  # noqa: BLE001
            logger.exception("Travel extraction via LLM failed; using fallback extraction.")
            from app.agents.fallback_data import fallback_travel_input

            return fallback_travel_input(user_input)
