from app.agents.base_agent import BaseAgent
from app.schemas.router import RouterResponse


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

        return self.router.invoke(prompt)
