import requests

params = {
    "engine": "google_hotels",
    "q": "Goa",
    "check_in_date": "2026-08-05",
    "check_out_date": "2026-08-10",
    "currency": "INR",
    "hl": "en",
    "api_key": ""
}

print(requests.get(
    "https://serpapi.com/search.json",
    params=params
).json())