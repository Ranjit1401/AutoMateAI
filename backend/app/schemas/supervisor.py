from typing import List, Literal
from pydantic import BaseModel


class AgentTask(BaseModel):
    """
    A single task assigned by the Supervisor.
    """

    agent: Literal["travel"]
    action: str


class SupervisorResponse(BaseModel):
    """
    Supervisor response containing all assigned tasks.
    """

    tasks: List[AgentTask]