"""Shared behavior for agents that need structured travel details pulled
out of the raw user message. Previously this exact extraction logic was
copy-pasted into both TravelAgent and ResearchAgent; now every agent that
needs it reuses one implementation."""
from app.prompts.travel_prompt import TRAVEL_PROMPT
from app.schemas.travel import TravelInput


class TravelExtractionMixin:
    """Mixin classes assume `self.llm` is provided by BaseAgent."""

    def _travel_parser(self):
        if not hasattr(self, "_cached_travel_parser"):
            self._cached_travel_parser = self.llm.with_structured_output(TravelInput)
        return self._cached_travel_parser

    def extract_travel(self, user_input: str) -> TravelInput:
        prompt = f"{TRAVEL_PROMPT}\n\nUser Request:\n{user_input}"
        return self._travel_parser().invoke(prompt)
