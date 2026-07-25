from app.agents.base_agent import BaseAgent
from app.schemas.planner import PlannerResponse  # <-- REQUIRED IMPORT


class PlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__()

        self.planner = self.llm.with_structured_output(
            PlannerResponse
        )

    def plan(self, user_input: str, task_type: str):

        prompt = f"""
You are an AI Planning Agent.

Task Type:
{task_type}

User Request:
{user_input}

Create an execution plan.
"""

        return self.planner.invoke(prompt)