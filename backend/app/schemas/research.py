from pydantic import BaseModel
from typing import List


class ResearchOutput(BaseModel):
    best_time: str
    top_places: List[str]
    local_food: List[str]