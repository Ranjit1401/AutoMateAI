from datetime import date, timedelta

from app.providers.serpapi_provider import serp_provider
from app.tools.base import BaseTool


# Add as many airports as you want (all keys should be lowercase)
AIRPORTS = {
    "mumbai": "BOM",
    "lucknow": "LKO",
    "goa": "GOI",
    "delhi": "DEL",
    "new delhi": "DEL",
    "bangalore": "BLR",
    "bengaluru": "BLR",
    "hyderabad": "HYD",
    "chennai": "MAA",
    "kolkata": "CCU",
    "pune": "PNQ",
    "ahmedabad": "AMD",
    "jaipur": "JAI",
    "kochi": "COK",
    "cochin": "COK",
    "surat": "STV",
    "nagpur": "NAG",
    "indore": "IDR",
    "bhopal": "BHO",
    "patna": "PAT",
    "varanasi": "VNS",
    "amritsar": "ATQ",
    "chandigarh": "IXC",
    "guwahati": "GAU",
    "srinagar": "SXR",
    "visakhapatnam": "VTZ",
    "trivandrum": "TRV",
}


class FlightTool(BaseTool):

    name = "flight"

    def execute(
        self,
        source,
        destination,
    ):

        # -------------------------
        # Normalize city names
        # -------------------------

        source = (source or "").strip().lower()
        destination = (destination or "").strip().lower()

        departure_airport = AIRPORTS.get(source)
        arrival_airport = AIRPORTS.get(destination)

        if not departure_airport:
            print(f"Unsupported source city: {source}")
            return []

        if not arrival_airport:
            print(f"Unsupported destination city: {destination}")
            return []

        departure = (
            date.today() + timedelta(days=7)
        ).isoformat()

        try:

            data = serp_provider.search_flights(
                departure_id=departure_airport,
                arrival_id=arrival_airport,
                outbound_date=departure,
            )

            print("=" * 70)
            print("RAW FLIGHT API RESPONSE")
            print(data)
            print("=" * 70)

            flights = []

            all_flights = (
                data.get("best_flights", [])
                + data.get("other_flights", [])
            )

            for offer in all_flights:

                if not offer.get("flights"):
                    continue

                segment = offer["flights"][0]

                price = offer.get("price", 0)

                if isinstance(price, str):
                    try:
                        price = float(
                            price.replace("₹", "")
                                 .replace(",", "")
                        )
                    except:
                        price = 0
                
                # Skip flights with missing/invalid price
                if not isinstance(price, (int, float)) or price <= 0:
                    continue
                
                flights.append({
                    "airline": segment.get("airline", "Unknown"),
                    "flight_number": segment.get("flight_number", ""),
                    "departure": segment.get("departure_airport", {}).get("time", ""),
                    "arrival": segment.get("arrival_airport", {}).get("time", ""),
                    "duration": offer.get("total_duration", ""),
                    "price": price,
                })

            # Cheapest flights first
            flights.sort(key=lambda x: x["price"])

            return flights[:5]

        except Exception as e:

            import traceback

            print("=" * 70)
            print("FLIGHT TOOL ERROR")
            traceback.print_exc()
            print("=" * 70)

            return []