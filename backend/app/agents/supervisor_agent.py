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

            step_lower = step.lower()

            if "activities" in step_lower:
                agent = "research"
            
            elif "itinerary" in step_lower:
                agent = "itinerary"
            
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