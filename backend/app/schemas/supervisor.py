from typing import List, Literal
from pydantic import BaseModel


class AgentTask(BaseModel):
    agent: Literal[
        "travel",
        "research",
        "coding",
        "email",
        "calendar",
        "shopping",
        "finance",
        "memory"
    ]

    action: str


class SupervisorResponse(BaseModel):
    tasks: List[AgentTask]