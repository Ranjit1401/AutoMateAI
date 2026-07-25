from app.core.llm import llm
from app.schemas.planner import PlannerResponse


class PlannerAgent:

    def __init__(self):

        self.planner = llm.with_structured_output(
            PlannerResponse
        )

    def plan(
        self,
        user_input: str,
        task_type: str
    ) -> PlannerResponse:

        prompt = f"""
You are an AI Planning Agent.

Task Category:
{task_type}

User Request:
{user_input}

Your job is to create an execution plan.

Rules:

1. Understand the user's goal.
2. Estimate complexity.
3. Decide which AI agents are needed.
4. Create logical execution steps.

Keep steps concise.
"""

        return self.planner.invoke(prompt)