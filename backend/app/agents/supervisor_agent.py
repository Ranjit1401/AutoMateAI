from app.agents.base_agent import BaseAgent
from app.schemas.supervisor import SupervisorResponse, AgentTask
from app.agents.budget_agent import BudgetAgent


class SupervisorAgent(BaseAgent):

    def __init__(self):
        super().__init__()

    def decide(self, goal: str, steps: list[str]) -> SupervisorResponse:
        """
        Assign planner steps to the appropriate agent.
        """

        tasks = []

        for step in steps:

            step_lower = step.lower()

            if "activities" in step_lower:
                agent = "research"

            elif "itinerary" in step_lower:
                agent = "itinerary"

            elif "budget" in step_lower:
                agent = "budget"

            else:
                agent = "travel"
            
            tasks.append(
                AgentTask(
                    agent=agent,
                    action=step
                )
            )
            print("=" * 60)
            print("SUPERVISOR")
            print("STEP :", step)
            print("AGENT:", agent)
            print("=" * 60)

        # IMPORTANT: Return the response
        return SupervisorResponse(tasks=tasks)

        