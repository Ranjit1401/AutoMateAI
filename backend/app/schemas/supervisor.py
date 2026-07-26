from typing import Literal

from pydantic import BaseModel

AgentName = Literal[
    "travel",
    "research",
    "itinerary",
    "budget",
    "restaurant",
    "maps",
    "booking",
]


class AgentTask(BaseModel):
    agent: AgentName
    action: str


class SupervisorResponse(BaseModel):
    tasks: list[AgentTask]
