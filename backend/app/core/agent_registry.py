from app.agents.router_agent import RouterAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.supervisor_agent import SupervisorAgent
from app.agents.travel_agent import TravelAgent
from app.agents.response_agent import ResponseAgent


class AgentRegistry:

    def __init__(self):
        self._agents = {}

        # Register all agents
        self.register("router", RouterAgent())
        self.register("planner", PlannerAgent())
        self.register("supervisor", SupervisorAgent())
        self.register("travel", TravelAgent())
        self.register("response", ResponseAgent())

    def register(self, name: str, agent):
        self._agents[name] = agent

    def get(self, name: str):
        return self._agents.get(name)

    def list_agents(self):
        return list(self._agents.keys())


# Global registry instance
registry = AgentRegistry()