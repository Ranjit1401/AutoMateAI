from app.providers.serpapi_provider import serp_provider
from app.tools.base import BaseTool


class HotelTool(BaseTool):

    name = "hotel"

    def execute(
        self,
        destination,
        check_in_date,
        check_out_date,
        max_price=None,
        min_rating=4.0,
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

        for hotel in data.get("properties", []):

            price = hotel.get("rate_per_night", {}).get("lowest")
            rating = hotel.get("overall_rating", 0)

            # Convert price to float
            if isinstance(price, str):
                try:
                    price = float(
                        price.replace("₹", "")
                             .replace(",", "")
                    )
                except:
                    continue

            if price is None:
                continue

            if rating is None:
                rating = 0

            # Rating filter
            if rating < min_rating:
                continue

            # Budget filter (optional)
            if max_price is not None and price > max_price:
                continue

            hotels.append({
                "name": hotel.get("name"),
                "price": price,
                "rating": rating,
            })

        # Sort by cheapest first
        hotels.sort(key=lambda x: x["price"])

        # Return top 5
        return hotels[:5]