from app.agents.base_agent import BaseAgent
from app.core.logging_config import get_logger
from app.schemas.router import RouterResponse

logger = get_logger(__name__)


class RouterAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.router = self.llm.with_structured_output(RouterResponse)

    def route(self, user_input: str) -> RouterResponse:
        prompt = f"""Classify the user's request into one category.

Categories:
travel
coding
shopping
research
document
email
calendar
finance
general

User Request:
{user_input}"""

        try:
            return self.router.invoke(prompt)
        except Exception:  # noqa: BLE001 - LLM unavailable must not crash the pipeline
            logger.exception("Router LLM call failed; using fallback classification.")
            from app.agents.fallback_data import fallback_router_response

            return fallback_router_response()
