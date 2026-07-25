from app.agents.base_agent import BaseAgent
from app.schemas.supervisor import SupervisorResponse, AgentTask


class SupervisorAgent(BaseAgent):

    def __init__(self):
        super().__init__()

    def decide(self, goal: str, steps: list[str]) -> SupervisorResponse:
        """
        Assign planner steps to the appropriate agent.
        """

        tasks = []

        for step in steps:

            if "activities" in step.lower():
                agent = "research"
            else:
                agent = "travel"

            tasks.append(
                AgentTask(
                    agent=agent,
                    action=step
                )
            )

        # IMPORTANT: Return the response
        return SupervisorResponse(tasks=tasks)