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
from app.schemas.memory_extraction import MemoryExtraction


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
        return self._parser.invoke(prompt)
