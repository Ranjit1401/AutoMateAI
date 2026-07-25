from typing import Optional

from pydantic import BaseModel, Field


class TravelInput(BaseModel):

    source: Optional[str] = Field(
        default=None,
        description="Starting city"
    )

    destination: str = Field(
        description="Destination city"
    )

    budget: Optional[int] = Field(
        default=None,
        description="Total trip budget"
    )

    travellers: int = Field(
        default=1,
        description="Number of travellers"
    )

    days: int = Field(
        default=3,
        description="Number of days for the trip"
    )

    start_date: Optional[str] = Field(
        default=None,
        description="Trip start date in YYYY-MM-DD format"
    )

    end_date: Optional[str] = Field(
        default=None,
        description="Trip end date in YYYY-MM-DD format"
    )