from datetime import date, datetime

from app.agents.base_agent import BaseAgent
from app.agents.mixins import TravelExtractionMixin
from app.tools.executor import ToolExecutionError, tool_executor


def _nights_between(start_date: str | None, end_date: str | None, default: int = 3) -> int:
    if not start_date or not end_date:
        return default
    try:
        start = datetime.fromisoformat(start_date).date()
        end = datetime.fromisoformat(end_date).date()
        return max((end - start).days, 1)
    except ValueError:
        return default


def _cheapest_price(offers: list[dict], key: str = "price") -> float:
    prices = [o[key] for o in offers if isinstance(o.get(key), (int, float))]
    return min(prices) if prices else 0.0


class BudgetAgent(BaseAgent, TravelExtractionMixin):
    """Reuses whatever flight/hotel results earlier steps in this run
    already produced (to avoid a redundant paid API call), falls back to
    fetching them itself, then runs the real budget_calculator tool."""

    def execute(self, action: str, state: dict) -> dict:
        travel = self.extract_travel(state["user_input"])

        flights, hotels = self._reuse_or_fetch(travel)
        nights = _nights_between(travel.start_date, travel.end_date)

        try:
            budget = tool_executor.execute(
                "budget_calculator",
                flight_total=_cheapest_price(flights) * travel.travellers,
                hotel_price_per_night=_cheapest_price(hotels),
                nights=nights,
                travellers=travel.travellers,
                tier="mid",
            )
        except ToolExecutionError as exc:
            return {"action": action, "budget": None, "error": exc.message}

        return {"action": action, "budget": budget}

    @staticmethod
    def _reuse_or_fetch(travel) -> tuple[list[dict], list[dict]]:
        flights: list[dict] = []
        hotels: list[dict] = []

        try:
            flights = tool_executor.execute("flight", source=travel.source or "Mumbai", destination=travel.destination)
        except ToolExecutionError:
            flights = []

        try:
            hotels = tool_executor.execute("hotel", destination=travel.destination)
        except ToolExecutionError:
            hotels = []

        return flights, hotels
