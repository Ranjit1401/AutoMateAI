from app.core.llm import llm
from app.schemas.router import RouterResponse


class RouterAgent:

    def __init__(self):
        self.router_llm = llm.with_structured_output(RouterResponse)

    def route(self, user_input: str) -> RouterResponse:

        prompt = f"""
Classify the user's request into exactly one of these categories:

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
{user_input}
"""

        return self.router_llm.invoke(prompt)