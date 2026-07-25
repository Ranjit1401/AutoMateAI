from app.agents.base_agent import BaseAgent
from app.schemas.supervisor import SupervisorResponse, AgentTask


class SupervisorAgent(BaseAgent):

    def __init__(self):
        super().__init__()

    def decide(self, goal: str, steps: list[str]) -> SupervisorResponse:
        """
        For the MVP, every planner step is assigned to the Travel Agent.
        """

        tasks = []

        for step in steps:
            tasks.append(
                AgentTask(
                    agent="travel",
                    action=step
                )
            )

        return SupervisorResponse(tasks=tasks)