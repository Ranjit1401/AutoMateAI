from app.providers.serpapi_provider import serp_provider
from app.tools.base import BaseTool


class HotelTool(BaseTool):

    name = "hotel"

    def execute(
        self,
        destination,
        check_in_date,
        check_out_date,
    ):

        data = serp_provider.search_hotels(
            destination,
            check_in_date,
            check_out_date,
        )

        print("=" * 60)
        print("RAW HOTEL API RESPONSE")
        print(data)
        print("=" * 60)

        hotels = []

        for hotel in data.get("properties", [])[:5]:

            hotels.append({
                "name": hotel.get("name"),
                "price": hotel.get("rate_per_night", {}).get("lowest"),
                "rating": hotel.get("overall_rating"),
            })

        return hotels