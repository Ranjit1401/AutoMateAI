from pydantic import BaseModel, Field


class DestinationResearch(BaseModel):
    summary: str = Field(description="A 1-2 sentence overview of the destination")
    top_places: list[str] = Field(description="4-6 must-visit places or attractions")
    local_food: list[str] = Field(description="3-5 local dishes worth trying")
    best_time_to_visit: str = Field(description="Best months/season to visit, briefly")
