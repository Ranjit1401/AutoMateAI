import requests

API_KEY = ""

url = "https://serpapi.com/search.json"

params = {
    "engine": "google_flights",
    "departure_id": "BOM",
    "arrival_id": "GOI",
    "outbound_date": "2026-08-05",
    "return_date": "2026-08-10",
    "currency": "INR",
    "hl": "en",
    "api_key": API_KEY,
}

response = requests.get(url, params=params)

print(response.status_code)
print(response.json())