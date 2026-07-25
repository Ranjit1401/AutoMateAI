from typing import Literal
from pydantic import BaseModel


class AgentTask(BaseModel):
    agent: Literal[
        "travel",
        "research",
        "itinerary",
        "budget"
    ]
    action: str


class SupervisorResponse(BaseModel):
    tasks: list[AgentTask]