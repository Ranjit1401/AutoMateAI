from app.providers.serpapi_provider import serp_provider
from app.tools.base import BaseTool, ToolError


class HotelTool(BaseTool):
    name = "hotel"
    description = "Searches live hotel listings for a destination."

    def execute(self, destination: str) -> list[dict]:
        try:
            data = serp_provider.search_hotels(destination)
        except Exception as exc:  # noqa: BLE001
            raise ToolError(f"Hotel search failed: {exc}") from exc

        hotels = []
        for hotel in data.get("properties", [])[:5]:
            hotels.append(
                {
                    "name": hotel.get("name"),
                    "price": hotel.get("rate_per_night", {}).get("lowest"),
                    "rating": hotel.get("overall_rating"),
                }
            )
        return hotels
