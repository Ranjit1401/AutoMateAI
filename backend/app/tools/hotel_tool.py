from app.providers.serpapi_provider import serp_provider
from app.tools.base import BaseTool


class HotelTool(BaseTool):

    name = "hotel"

    def execute(self, destination):

        data = serp_provider.search_hotels(destination)

        hotels = []

        for hotel in data.get("properties", [])[:5]:

            hotels.append({
                "name": hotel.get("name"),
                "price": hotel.get("rate_per_night", {}).get("lowest"),
                "rating": hotel.get("overall_rating"),
            })

        return hotels