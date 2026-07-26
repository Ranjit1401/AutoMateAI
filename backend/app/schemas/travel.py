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

    start_date: Optional[str] = None

    end_date: Optional[str] = None

    travellers: int = 1