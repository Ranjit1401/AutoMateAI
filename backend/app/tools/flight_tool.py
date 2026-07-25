from datetime import date, timedelta

from app.providers.serpapi_provider import serp_provider
from app.tools.base import BaseTool


AIRPORTS = {
    "Mumbai": "BOM",
    "Goa": "GOI",
    "Delhi": "DEL",
    "Bangalore": "BLR",
    "Hyderabad": "HYD",
    "Chennai": "MAA",
}


class FlightTool(BaseTool):

    name = "flight"

    def execute(
        self,
        source,
        destination,
    ):

        departure = (
            date.today() + timedelta(days=7)
        ).isoformat()

        try:

            data = serp_provider.search_flights(
                departure_id=AIRPORTS[source],
                arrival_id=AIRPORTS[destination],
                outbound_date=departure,
            )

            flights = []

            all_flights = (
                data.get("best_flights", [])
                + data.get("other_flights", [])
            )

            for offer in all_flights[:5]:

                segment = offer["flights"][0]

                flights.append({

                    "airline":
                        segment["airline"],

                    "flight_number":
                        segment["flight_number"],

                    "departure":
                        segment["departure_airport"]["time"],

                    "arrival":
                        segment["arrival_airport"]["time"],

                    "duration":
                        offer["total_duration"],

                    "price":
                        offer.get("price", "N/A")

                })

            return flights

        except Exception as e:

            print("Flight Tool:", e)

            return []