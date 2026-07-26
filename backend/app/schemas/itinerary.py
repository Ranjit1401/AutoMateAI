from pydantic import BaseModel, Field


class ItineraryDay(BaseModel):
    day: int
    theme: str = Field(description="Short theme for the day, e.g. 'Old town & food crawl'")
    activities: list[str] = Field(description="3-5 ordered activities for the day")


class ItineraryPlan(BaseModel):
    days: list[ItineraryDay]
