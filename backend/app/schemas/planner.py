from typing import List, Literal

from pydantic import BaseModel


class PlannerResponse(BaseModel):

    goal: str

    estimated_complexity: Literal[
        "easy",
        "medium",
        "hard"
    ]

    required_agents: List[str]

    steps: List[str]