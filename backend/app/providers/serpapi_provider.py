import os
from datetime import datetime, timedelta
from serpapi import GoogleSearch


class Cache:

    def __init__(self):
        self.cache = {}
        self.expiry = timedelta(hours=1)

    def get(self, key):

        if key not in self.cache:
            return None

        value, timestamp = self.cache[key]

        if datetime.now() - timestamp > self.expiry:
            del self.cache[key]
            return None

        return value

    def set(self, key, value):

        self.cache[key] = (
            value,
            datetime.now()
        )


cache = Cache()


class SerpAPIProvider:

    def __init__(self):

        self.api_key = os.getenv("SERPAPI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "SERPAPI_API_KEY not found in environment variables."
            )

    ####################################################################
    # Flights
    ####################################################################

    def search_flights(
        self,
        departure_id: str,
        arrival_id: str,
        outbound_date: str,
    ):
    
        outbound = datetime.strptime(
            outbound_date,
            "%Y-%m-%d"
        )
    
        return_date = (
            outbound + timedelta(days=5)
        ).strftime("%Y-%m-%d")
    
        cache_key = (
            f"flight-"
            f"{departure_id}-"
            f"{arrival_id}-"
            f"{outbound_date}"
        )
    
        cached = cache.get(cache_key)
    
        if cached:
            print("✅ Flight cache hit")
            return cached
    
        params = {
            "engine": "google_flights",
            "departure_id": departure_id,
            "arrival_id": arrival_id,
            "outbound_date": outbound_date,
            "return_date": return_date,
            "currency": "INR",
            "hl": "en",
            "api_key": self.api_key,
        }
    
        try:
        
            search = GoogleSearch(params)
    
            results = search.get_dict()
    
            cache.set(cache_key, results)
    
            return results
    
        except Exception as e:
        
            print(e)
    
            return {}

    ####################################################################
    # Hotels
    ####################################################################

    def search_hotels(
        self,
        location: str,
        check_in_date=None,
        check_out_date=None,
    ):

        cache_key = f"hotel-{location}"

        cached = cache.get(cache_key)

        if cached:
            print("✅ Hotel cache hit")
            return cached

        params = {
            "engine": "google_hotels",
            "q": location,
            "currency": "INR",
            "hl": "en",
            "api_key": self.api_key,
        }

        if check_in_date:
            params["check_in_date"] = check_in_date

        if check_out_date:
            params["check_out_date"] = check_out_date

        try:

            search = GoogleSearch(params)

            results = search.get_dict()

            cache.set(cache_key, results)

            return results

        except Exception as e:

            print(f"[SerpAPI Hotel Error] {e}")

            return {}

    ####################################################################
    # Places
    ####################################################################

    def search_places(
        self,
        query: str,
    ):

        cache_key = f"places-{query}"

        cached = cache.get(cache_key)

        if cached:
            print("✅ Places cache hit")
            return cached

        params = {
            "engine": "google",
            "q": query,
            "hl": "en",
            "api_key": self.api_key,
        }

        try:

            search = GoogleSearch(params)

            results = search.get_dict()

            cache.set(cache_key, results)

            return results

        except Exception as e:

            print(f"[SerpAPI Places Error] {e}")

            return {}


serp_provider = SerpAPIProvider()