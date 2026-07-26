"""
Long-term memory extraction. After each user turn, the chat pipeline asks
this agent whether the message contained a durable fact worth remembering
(a stated preference, a recurring constraint, etc). If so, app/api/chat.py
persists it to the MemoryEntry table, and future turns retrieve relevant
memories and feed them back into the agents' prompts — closing the loop
that was previously broken (conversation_history was stored but never
actually read by any agent).
"""
from app.agents.base_agent import BaseAgent
from app.core.logging_config import get_logger
from app.schemas.memory_extraction import MemoryExtraction

logger = get_logger(__name__)


class MemoryAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self._parser = self.llm.with_structured_output(MemoryExtraction)

    def extract(self, user_input: str) -> MemoryExtraction:
        prompt = (
            "Decide whether this message states a durable fact or preference about "
            "the user that would be useful to remember in future conversations.\n\n"
            f"Message:\n{user_input}"
        )
        try:
            return self._parser.invoke(prompt)
        except Exception:  # noqa: BLE001 - memory extraction is best-effort
            logger.exception("Memory extraction LLM call failed; skipping this turn.")
            from app.agents.fallback_data import fallback_memory_extraction

            return fallback_memory_extraction()
