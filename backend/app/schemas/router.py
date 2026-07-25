from typing import Literal
from pydantic import BaseModel


class RouterResponse(BaseModel):

    task_type: Literal[
        "travel",
        "coding",
        "shopping",
        "research",
        "document",
        "email",
        "calendar",
        "finance",
        "general"
    ]

    reason: str