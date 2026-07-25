from app.agents.base_agent import BaseAgent
from app.schemas.supervisor import SupervisorResponse


class SupervisorAgent(BaseAgent):

    def __init__(self):
        super().__init__()

        self.supervisor = self.llm.with_structured_output(
            SupervisorResponse
        )

    def decide(self, goal: str, steps: list[str]):

        prompt = f"""
You are an AI Supervisor.

Goal:
{goal}

Execution Steps:
{steps}

Choose which specialized AI agent should perform each step.

Rules:
- Return one task per step.
- Use ONLY these agents:
travel
research
coding
email
calendar
shopping
finance
memory

Return structured output.
"""

        return self.supervisor.invoke(prompt)