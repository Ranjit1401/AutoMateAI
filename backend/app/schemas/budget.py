from pydantic import BaseModel


class BudgetSummary(BaseModel):
    flight_cost: float
    hotel_cost: float
    food_cost: float
    transport_cost: float
    activities_cost: float

    total_cost: float

    budget: float

    remaining_budget: float

    within_budget: bool

    suggestions: list[str]