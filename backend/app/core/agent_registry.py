"""Registers every agent exactly once. The old duplicate flight/hotel
*tool* registrations that used to live here (this file used to register
FlightTool/HotelTool alongside agents, mixing two different concepts) have
been removed — tools are registered in app/tools/__init__.py only."""
from app.agents.booking_agent import BookingAgent
from app.agents.budget_agent import BudgetAgent
from app.agents.itinerary_agent import ItineraryAgent
from app.agents.maps_agent import MapsAgent
from app.agents.memory_agent import MemoryAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.research_agent import ResearchAgent
from app.agents.response_agent import ResponseAgent
from app.agents.restaurant_agent import RestaurantAgent
from app.agents.router_agent import RouterAgent
from app.agents.supervisor_agent import SupervisorAgent
from app.agents.travel_agent import TravelAgent


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, object] = {}
        self.register("router", RouterAgent())
        self.register("planner", PlannerAgent())
        self.register("supervisor", SupervisorAgent())
        self.register("travel", TravelAgent())
        self.register("research", ResearchAgent())
        self.register("itinerary", ItineraryAgent())
        self.register("budget", BudgetAgent())
        self.register("restaurant", RestaurantAgent())
        self.register("maps", MapsAgent())
        self.register("booking", BookingAgent())
        self.register("response", ResponseAgent())
        self.register("memory", MemoryAgent())

    def register(self, name: str, agent) -> None:
        self._agents[name] = agent

    def get(self, name: str):
        return self._agents.get(name)

    def list_agents(self) -> list[str]:
        return list(self._agents.keys())


registry = AgentRegistry()
